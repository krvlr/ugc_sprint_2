# Проектная работа 9-го спринта
---

https://github.com/krvlr/ugc_sprint_2

[![Build status](https://github.com/krvlr/ugc_sprint_2/actions/workflows/python.yml/badge.svg?branch=main)](https://github.com/krvlr/ugc_sprint_2/actions/workflows/python.yml)

Исследование производительности Mongo vs Postgresql находится в db_research

Реализован сервис выставления оценок фильмам, отзывов и закладок

Реализованы следующие `endpoint`-ы:

- `/api/v1/ugc2/ratings/` - оценки фильмов пользователя,
- `/api/v1/ugc2/ratings/create` - поставить оценку фильму,
- `/api/v1/ugc2/ratings/update` - обновить оценку,
- `/api/v1/ugc2/ratings/delete?film_id=<film_id>` - удалить оценку фильма,
- `/api/v1/ugc2/ratings/count/<film_id>` - количество оценок у фильма,
- `/api/v1/ugc2/ratings/avg/<film_id>` - средняя оценка у фильма,
- `/api/v1/ugc2/bookmarks/` - закладки фильмов пользователя,
- `/api/v1/ugc2/bookmarks/create` - создать закладку фильма,
- `/api/v1/ugc2/bookmarks/delete?film_id=<film_id>` - удалить закладку фильма,
- `/api/v1/ugc2/reviews/` - обзоры фильмов,
- `/api/v1/ugc2/reviews/create` - создать обзор фильма,
- `/api/v1/ugc2/reviews/update` - обновить обзор,
- `/api/v1/ugc2/reviews/delete?film_id=<film_id>` - удалить обзор фильма,

В рамках данного репозитория также реализованы следующие сервисы:

- Сервис авторизации
- Сервис получения информации о фильмах
- Сервис для управления подписками
- Сервис для работы с данными о прогрессе просмотра кино

В рамках сервиса авторизации реализованы следующие `endpoint`-ы:

- `/api/v1/signup` - регистрация пользователя,
- `/api/v1/signin` - вход в аккаунт,
- `/api/v1/refresh` - получение свежего `Acccess` токена аутентифицированным пользователем (при наличии свежего и неиспользованного `Refresh` токена),
- `/api/v1/password/change` - изменение пароля аутентифицированного пользователя,
- `/api/v1/signout` - выход из устройства аутентифицированным пользователем (при наличии свежего `Acccess` токена),
- `/api/v1/signout/all` - выход из устройства аутентифицированным пользователем (при наличии свежего `Acccess` токена).
- `/api/v1/history` - получение списка действий текущего аутентифицированного пользователя (при наличии свежего `Acccess` токена),
- `/api/v1/google/signin`, `/api/v1/google/callback` - вход в google аккаунт,
- `/api/v1/yandex/signin`, `/api/v1/yandex/callback` - вход в yandex аккаунт.

В рамках сервиса управления подписками реализованы следующие `endpoint`-ы:

- `/api/v1/roles/create_role` - создание подписки,
- `/api/v1/roles/delete_role/<name>` - удаление подписки,
- `/api/v1/roles/role_details/<name>` - получение информации по подписке,
- `/api/v1/roles/roles_details` - получение информации по всем актуальным подпискам,
- `/api/v1/roles/modified_role/<name>` - изменение подписки,
- `/api/v1/roles/add_user_role/<name>` - добавление подписки пользователю,
- `/api/v1/roles/delete_user_role/<name>` - удаление подписки у пользователя,
- `/api/v1/roles/check_user_role/<name>` - проверка наличия подписки у пользователя.

В рамках сервиса получения информации о фильмах реализованы следующие `endpoint`-ы:

- TBD

В рамках онлайн-кинотеатра предусмотрена система подписок. При регистрации пользователю выдается `default` подписка.

Cервис авторизации предоставляет возможность аутентифицировать и авторизовать клиента с помощью активного `Access` токена.  
Для возможности проверить права пользователя на получение доступа к определенному контенту, в `payload` токена заложены: 
- Права и роль пользователя, 
- Список активных подписок.

При наличии секретного ключа, необходимого для проверки подписи активного `Access`-токена, каждый из микросервисов онлайн-кинотеатра сможет аутентифицировать и авторизовать пользователя.

При регистрации клиент получает роль `пользователя` (`is_admin = False`), а также стандартную подписку.

За создание и состав подписок будет отвечать отдельный сервис (TBD). В рамках которого, у его администраторов, будет возможность создавать и реализовывать бизнес-логику подписок. 

Для создания администраторов сервиса авторизации необходимо выполнить следующую команду из терминала:
    
    docker compose exec api-auth flask --app main create_admin <login> <email> <password>

## Описание структуры репозитория:
---

1. `db` — раздел с настройками базы `PostgreSQL`.
2. `flask_auth` — раздел с описанием сервиса авторизации.
3. `nginx` — раздел с описанием настроек `nginx` для сервиса авторизации.

## Пример запуска
---

Перед запуском контейнеров, в корне `/` необходимо создать файл `.env` (в качестве примера `.env.example`):

    touch .env

А также указать в нем значения следующих переменных окружения:

    AUTH_DB_HOST
    AUTH_DB_PORT
    AUTH_DB_NAME
    AUTH_DB_USER
    AUTH_DB_PASSWORD
    AUTH_REDIS_HOST
    AUTH_REDIS_PORT
    FLASK_SECRET_KEY
    JWT_COOKIE_SECURE
    JWT_TOKEN_LOCATION
    JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES
    INITIAL_USER_ROLES
    INITIAL_USER_DESCRIPTION_ROLES
    DEFAULT_USER_ROLE
    JAEGER_HOST
    JAEGER_PORT
    AUTH_HEALTHCHECK_REQUEST_ID
    REQUEST_LIMIT_PER_MINUTE
    LOGGING_LEVEL
    LOG_FORMAT
    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET
    GOOGLE_CONF_URL
    YANDEX_CLIENT_ID
    YANDEX_CLIENT_SECRET
    YANDEX_ACCESS_TOKEN_URL
    YANDEX_AUTHORIZE_URL
    YANDEX_USER_INFO_URL
    KAFKA_HOST=broker
    KAFKA_PORT
    CLICKHOUSE_HOST
    CLICKHOUSE_ALT_HOSTS
    KAFKA_TOPICS
    KAFKA_EXTRACT_NUM_MESSAGES
    KAFKA_EXTRACT_TIMEOUT
    KAFKA_GROUP_ID
    KAFKA_AUTO_OFFSET_RESET
    MONGODB_HOST
    MONGODB_PORT
    MONGODB_LOGIN
    MONGODB_PASSWORD
    MONGODB_DB_NAME
    MONGODB_COLLECTION_BOOKMARK
    MONGODB_COLLECTION_REVIEW

Теперь можно запустить сборку образа и запуск контейнеров:

    docker compose up -d --build

Чтобы остановить и полностью удалить контейнеры со всеми `volume` и `network`, описанными в рамках `docker-compose.yml`:

    docker-compose down --rmi all -v --remove-orphans

## Миграции
---

Первым шагом необходимо перейти в дирректорию c точкой входа (`main.py`):

    cd /flask_auth/src/

Для генерации миграций структуры таблиц, описание которых находится в дирректории `/flask_auth/src/db/models` необходимо выполнить следующую команду:
    
    flask --app main db migrate -m "Описание миграции"

Для применения сформированной миграции необхожимо выполнить следующую команду:
    
    flask --app main db upgrade

## Тестирование
---

Для запуска тестирования необходимо перейти в папку с тестами:

    cd flask_auth/tests/functional/

создать файл `.env` (в качестве примера `flask_auth/tests/functional/.env.example`):

    touch .env

указать в нем значения тех же переменных окружения, что и для основного `docker-compose`,
создать файл `.env.tests` (в качестве примера `flask_auth/tests/functional/.env.tests.example`):

    touch .env.tests

указать в нем значения следующих переменных окружения:

    AUTH_DB_HOST
    AUTH_DB_PORT
    AUTH_DB_NAME
    AUTH_DB_USER
    AUTH_DB_PASSWORD
    AUTH_DB_TABLES
    AUTH_REDIS_HOST
    AUTH_REDIS_PORT
    AUTH_API_HOST
    AUTH_API_PORT
    AUTH_API_URI
    AUTH_API_PROTOCOL

И запустить сборку образа и запуск контейнеров для тестирования:

    docker compose up --build

Если в логах будет сообщение об успешном прохождении тестирования - значит пришел успех!

## Настройка flake8 и pre-commit hook
---

Сформируем виртуальное `Python`-окружение в корне:

    python3 -m venv env

Активируем сформированное виртуальное `Python`-окружение:

    . env/bin/activate

Обновим `pip`:

    pip install --upgrade pip

Установим зависимости проекта:

    pip install -r requirements.txt

Установим `pre-commit hook`:

    pre-commit install

## CI-CD
---

TBD: В `GitHub actions` настроен запуск линтера и тестов при событии `push`.
