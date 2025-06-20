from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class ProjectSettings(BaseSettings):
    debug: bool = False
    name: str
    summary: str
    version: str
    terms_of_service: str
    tags: list = Field(
        default=[
            {
                "name": "recomended system",
                "description": "Operations with recomended system.",
            },
        ]
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="PROJECT_RECOM_")


class PostgresSettings(BaseSettings):
    """Настройки Postgres."""

    db: str
    host: str
    port: int
    user: str
    password: str
    dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="POSTGRES_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных"""

        self.dsn = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RedisSettings(BaseSettings):
    """Настройки Redis."""

    host: str
    port: int
    user: str
    password: str
    db_index: int
    dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="REDIS_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных."""

        self.dsn = f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_index}"


class RabbitConfig(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    vhost: str = "/"
    dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="RABBITMQ_")

    def model_post_init(self, __context):
        self.dsn = f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"


class SentrySettings(BaseSettings):
    """Настройки Sentry."""

    host: str
    port: int
    key: str
    dsn: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="SDK_SENTRY_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных."""

        self.dsn = f"http://{self.key}@{self.host}:{self.port}/1"


rabbitmq_settings = RabbitConfig()  # type: ignore
project_settings = ProjectSettings()  # type: ignore
postgres_settings = PostgresSettings()  # type: ignore
redis_settings = RedisSettings()  # type: ignore
sentry_settings = SentrySettings()  # type: ignore
