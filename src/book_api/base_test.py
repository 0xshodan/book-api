from rest_framework.test import APIRequestFactory, APIClient
from typing import TypeVar, Any
from django.db.models import Model
from rest_framework.serializers import BaseSerializer
from rest_framework.reverse import reverse_lazy

DEFAULT_LIST_COUNT = 20  # кол-во генерируемых обьектов модели для тестов

M = TypeVar("M", bound=Model)
S = TypeVar("S", bound=BaseSerializer)


def generate_list(count: int = DEFAULT_LIST_COUNT, **kwargs) -> list[dict]:
    ret: list[dict] = []
    for id in range(count):
        d = {}
        for k, v in kwargs.items():
            try:
                d[k] = v.format(id)
            except AttributeError:
                d[k] = v
        ret.append(d)
    return ret


def generate_models(model: M, count: int = DEFAULT_LIST_COUNT, **kwargs) -> list[M]:
    return [
        model.objects.create(**create_kwargs)
        for create_kwargs in generate_list(count, **kwargs)
    ]


class BaseEndpointTest:
    def __init__(
        self,
        client: APIClient,
        model_cls: M,
        serializer_cls: S,
        basename: str,
        fields: dict,
    ) -> None:
        self._client = client
        self._factory = APIRequestFactory()
        self._fields = fields
        self._model = model_cls
        self._serializer = serializer_cls
        self._basename = basename

    def test_list(self) -> None:
        models = generate_models(self._model, **self._fields)
        request = self._factory.get(reverse_lazy(f"{self._basename}-list"))
        response = self._client.get(reverse_lazy(f"{self._basename}-list"))
        data = self._serializer(data=response.data, many=True)
        assert data.is_valid()
        assert (
            self._serializer(models, many=True, context={"request": request}).data
            == data.initial_data
        )

    def test_create(self, **extra_fields) -> None:
        data = self._fields
        for k, v in extra_fields.items():
            data[k] = v
        for req_data in generate_list(count=DEFAULT_LIST_COUNT, **data):
            response = self._client.post(
                reverse_lazy(f"{self._basename}-list"), data=req_data
            )
            assert response.status_code == 201
        assert len(self._model.objects.all()) == DEFAULT_LIST_COUNT

    def test_create_failed(self, **incorrect_fields) -> None:
        data = self._fields
        for k, v in incorrect_fields.items():
            data[k] = v
        response = self._client.post(reverse_lazy(f"{self._basename}-list"), data=data)
        assert response.status_code == 400, response.data
        # self.assertEqual(response.data["first_name"][0].code, "blank")
        assert len(self._model.objects.all()) == 0

    def test_retrieve(self, compare_fields: list[str] = ["id"]) -> None:
        data = {"id": 1, **self._fields}
        self._model.objects.create(**self._fields)
        response = self._client.get(
            reverse_lazy(f"{self._basename}-detail", kwargs={"pk": 1})
        )
        assert response.status_code == 200, response.data
        for field in compare_fields:
            assert response.data[field] == data[field]

    def test_retrieve_failed(self) -> None:
        self._model.objects.create(**self._fields)
        response = self._client.get(
            reverse_lazy(f"{self._basename}-detail", kwargs={"pk": 999})
        )
        assert response.status_code == 404

    def test_update(self, **update_fields) -> None:
        data = self._fields.copy()
        for k, v in update_fields.items():
            data[k] = v
        self._model.objects.create(**self._fields)
        response = self._client.put(
            reverse_lazy(f"{self._basename}-detail", kwargs={"pk": 1}), data=data
        )
        assert response.status_code == 200, response.data

    def test_update_failed(self, **incorrect_fields) -> None:
        data = self._fields
        for k, v in incorrect_fields.items():
            data[k] = v
        self._model.objects.create(**self._fields)
        response = self._client.put(
            reverse_lazy(f"{self._basename}-detail", kwargs={"pk": 1}), data=data
        )
        assert response.status_code == 400, response.data

    def test_partial_update(self, **update_fields) -> None:
        data = self._fields.copy()
        for k, v in update_fields.items():
            data[k] = v
        self._model.objects.create(**self._fields)
        response = self._client.patch(
            reverse_lazy(f"{self._basename}-detail", kwargs={"pk": 1}), data=data
        )
        assert response.status_code == 200, response.data

    def test_partial_update_failed(self, **incorrect_fields) -> None:
        data = self._fields
        for k, v in incorrect_fields.items():
            data[k] = v
        self._model.objects.create(**self._fields)
        response = self._client.patch(
            reverse_lazy(f"{self._basename}-detail", kwargs={"pk": 1}), data=data
        )
        assert response.status_code == 400, response.data

    def test_destroy(self) -> None:
        self._model.objects.create(**self._fields)
        response = self._client.delete(
            reverse_lazy(f"{self._basename}-detail", kwargs={"pk": 1})
        )
        assert response.status_code == 204, response.data
        assert len(self._model.objects.all()) == 0

    def test_destroy_failed(self) -> None:
        self._model.objects.create(**self._fields)
        response = self._client.delete(
            reverse_lazy(f"{self._basename}-detail", kwargs={"pk": 999})
        )
        assert response.status_code == 404, response.data
        assert len(self._model.objects.all()) == 1
