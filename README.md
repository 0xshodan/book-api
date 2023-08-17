# Contact me:

[Telegram](https://t.me/cvvworldw1de)

Gmail: hngdean@gmail.com

Whatsapp: +79780544809

# Installation / Установка:

1. Clone repository:

```
git clone https://github.com/0xshodan/book-api
cd book-api
```

2. Configure .env file:

```
cp .env.example .env
```

## Docker

3. Need to install [docker compose](https://docs.docker.com/compose/)

4. Start docker compose:

```
docker compose up --build
```

or

```
docker-compose up --build
```

## Native

3. Need to install [poetry](https://python-poetry.org/docs/)
4. Install deps:

```
poetry install --only main
```

5. Activate virtualenv:

```
poetry shell
```

6. Run

```
cd src
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## FINISH:

GOTO: [swagger](http://localhost:8000/swagger/)
GOTO: [admin](http://localhost:8000/admin/)
GOTO: [drf-docs](http://localhost:8000/api/)
