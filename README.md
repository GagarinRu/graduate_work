# Рекомендательная система для онлайн-кинотеатра

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-orange?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-24.0-blue?logo=docker)
![Redis](https://img.shields.io/badge/Redis-7.0-red?logo=redis)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.9-purple?logo=rabbitmq)
![Kafka](https://img.shields.io/badge/Kafka-3.5-orange?logo=apachekafka)
![ClickHouse](https://img.shields.io/badge/ClickHouse-24.3-yellow?logo=clickhouse)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.8-green?logo=elasticsearch)
![JWT](https://img.shields.io/badge/JWT-authentication-yellow?logo=jsonwebtokens)


## 📚 Описание

Рекомендательная система предназначена для подбора фильмов, которые могут заинтересовать пользователя. Она может использоваться для отображения рекомендаций на фронтенде или формирования персонализированных рассылок.

## 🧩 Основные функции

Основные сервисы:
- **fastapi_auth**: Сервис аутентификации и авторизации пользователей с использованием JWT-токенов.
- **fastapi_ugc**: Сервис для сбора пользовательских данных (оценок фильмов).
- **fastapi_recom**: Сервис анализа пользовательских данных и формирование рекомендаций.
- **fastapi_ws**: Сервис для отправки уведомлений пользователю через WebSocket в реальном времени.
- **notifications_service**: Сервис уведомлений.

## 🛠 Технологический стек
- **FastAPI** — для создания REST API.
- **PostgreSQL** — для хранения данных.
- **RabbitMQ** — для асинхронного обмена сообщениями между сервисами.
- **FastStream** — для работы с брокером сообщений.
- **SQLAlchemy** — для взаимодействия с базой данных.
- **Aio-pika** — для асинхронной работы с RabbitMQ.
- **Alembic** — для управления миграциями базы данных.

## Актуальность данных
ETL-процесс обеспечивает постоянное обновление данных хранилище, гарантируя актуальность рекомендаций, включая информацию о фильмах, жанрах, актерах, режиссерах и других сущностях, даже при большом объеме пользовательских взаимодействий.


## Принцип работы

### Сбор и подготовка данных
1. Пользователь через сервис `fastapi_ugc` ставит оценку фильму.
2. Данные отправляются через RabbitMQ в сервис `fastapi_recom`.
3. Сервис `fastapi_recom` сохраняет данные в PostgreSQL для последующего анализа.
4. На основе собранных данных и схожести оценок пользователей формируются рекомендации.

### Получение рекомендаций
1. По эндпоинту `/recom/v1/user/{user_id}` можно получить рекомендации для конкретного пользователя.
2. Через RabbitMQ ставится задача на отправку уведомления (реализовано в качестве примера).
3. Сервис `fastapi_ws` принимает задачу и отправляет рекомендации пользователю.

## Требования
- Docker и Docker Compose
- Python 3.10+
- PostgreSQL 13+
- RabbitMQ 3.9+

## 🧰 Инструкция по запуску

### 1. Подготовка

1. Склонируйте репозиторий:
```bash
git clone https://github.com/GagarinRu/graduate_work.git
cd graduate_work
```
2. Создайте `.env` файл из шаблона:

```python
cp .env.example .env
```

Настройте параметры подключения к БД, Redis, JWT и другим сервисам.

### 2. Запуск контейнеров

1. Убедитесь, что Docker и Docker Compose установлены.
2. Запустите сервисы с помощью Docker Compose:
```bash
docker-compose -f docker-compose.yml up --build
```

### 3. Регистрация пользователя

Перейти на страницу Swagger.
```bash
curl http://localhost/auth/openapi
```
Создать пользователя(/auth/v1/register) и получить JWT-токен(/auth/v1/jwt/login)

### 4. Работа с пуш уведомлениями(почта, чат-комната)

На почту,указанную при регистрации прийдет письмо с короткой ссылки для подтверждения пользователя и создания Чат-комнаты Websocket.
Перейти в чат-комнату Websocket по почте.

```bash
curl http://localhost/ws/v1/chat/
```

В дальнейшем по указанному почтовому адресу на почту и в чат-комнату будут приходить рассылки с рекомендациями.

### 4. Работа с рекомендациями

```bash
curl http://localhost/recom/v1/user/{user_id}
```

## Пример использования
Для получения рекомендаций для пользователя с `user_id=a1b4cc23-e559-49c8-898d-8e8c37e6f489` выполните:
```bash
curl http://localhost/recom/v1/user/a1b4cc23-e559-49c8-898d-8e8c37e6f489
```

Пример ответа:
```json
{
  "user_id": "a1b4cc23-e559-49c8-898d-8e8c37e6f489",
  "recommendations": [
    {"movie_id": "d00502db-dcd6-49de-b7ed-5ca8dc89a2fb"},
    {"movie_id": "481dccec-447f-4e26-8df6-9396785f3eb7"}
  ]
}
```

## Тестирование
Для проверки работоспособности системы:
1. Убедитесь, что все сервисы запущены.
2. Отправьте тестовую оценку через эндпоинт сервиса `fastapi_ugc`.
3. Проверьте получение рекомендаций через эндпоинт `/recom/v1/user/{user_id}`.


📢 Авторы:

Alex Mishakovhttps://github.com/AlexMishakov

Evgeny Kudryashov: https://github.com/

Ivlev Alexey: https://github.com/Theivlev
