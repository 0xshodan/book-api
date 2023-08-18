from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from datetime import date
from rest_framework.test import APITestCase
from book_api.base_test import BaseEndpointTest
from django.contrib.auth.models import User


class AuthorEndpointTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_class = BaseEndpointTest

    def setUp(self) -> None:
        self.test_class = BaseEndpointTest(
            self.client,
            Author,
            AuthorSerializer,
            "author",
            fields={
                "first_name": "{}Name",
                "last_name": "{}LastName",
                "date_of_birth": date.today(),
                "biography": "{}",
            },
        )
        self.user = User.objects.create_user(
            username="john", email="jlennon@beatles.com", password="glass onion"
        )
        self.client.force_authenticate(self.user)

    def test_list(self) -> None:
        self.test_class.test_list()

    def test_create(self) -> None:
        self.test_class.test_create()

    def test_create_failed(self) -> None:
        self.test_class.test_create_failed(first_name="")

    def test_update(self) -> None:
        self.test_class.test_update(first_name="dasds", last_name="dadsa")

    def test_update_failed(self) -> None:
        self.test_class.test_update_failed(first_name="")

    def test_partial_update(self) -> None:
        self.test_class.test_update(first_name="dasds", last_name="dadsa")

    def test_partial_update_failed(self) -> None:
        self.test_class.test_partial_update_failed(first_name="")

    def test_retrieve(self) -> None:
        self.test_class.test_retrieve(["id", "first_name", "last_name", "biography"])

    def test_retrieve_failed(self) -> None:
        self.test_class.test_retrieve_failed()

    def test_destroy(self) -> None:
        self.test_class.test_destroy()

    def test_destroy_failed(self) -> None:
        self.test_class.test_destroy()


class BookEndpointTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_class = BaseEndpointTest

    def setUp(self) -> None:
        self.test_class = BaseEndpointTest(
            self.client,
            Book,
            BookSerializer,
            "book",
            fields={
                "title": "{}title",
                "publication_date": date.today(),
                "description": "213",
                "author": Author(id=1, first_name="das", last_name="sad"),
            },
        )
        self.user = User.objects.create_user(
            username="john", email="jlennon@beatles.com", password="glass onion"
        )
        self.client.force_authenticate(self.user)

    def test_list(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_list()

    def test_create(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_create(author="/api/authors/1/")

    def test_create_failed(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_create_failed(title="")

    def test_update(self) -> None:
        author = Author(id=1, first_name="das", last_name="sad")
        author.save()
        self.test_class.test_update(
            title="dasds",
            description="dadsa",
            author="/api/authors/1/",
        )

    def test_update_failed(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_update_failed(title="")

    def test_partial_update(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_partial_update(
            title="dasds",
            description="dadsa",
            author="/api/authors/1/",
        )

    def test_partial_update_failed(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_partial_update_failed(title="")

    def test_retrieve(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_retrieve(["id", "title", "description"])

    def test_retrieve_failed(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_retrieve_failed()

    def test_destroy(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_destroy()

    def test_destroy_failed(self) -> None:
        Author(id=1, first_name="das", last_name="sad").save()
        self.test_class.test_destroy()
