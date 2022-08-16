import datetime
import functools

import pydantic


class App(pydantic.BaseSettings):
    APP_NAME: str = "Project Starter"
    DEV_MODE: bool = False
    LOCALES: list[str] = ["en"]
    API_URL: str = "/api/v1"


class Security(pydantic.BaseSettings):
    TOKEN_URL: str = "/token"
    REFRESH_TOKEN_URL: str = f"/{TOKEN_URL}/refresh"
    AUTHPASETO_SECRET_KEY: str
    AUTHPASETO_ACCESS_TOKEN_EXPIRES: datetime.timedelta = datetime.timedelta(minutes=30)
    AUTHPASETO_REFRESH_TOKEN_EXPIRES: datetime.timedelta = datetime.timedelta(days=1)
    AUTHPASETO_DENYLIST_ENABLED: bool = True
    AUTHPASETO_DENYLIST_TOKEN_CHECKS: set[str] = {"access", "refresh"}
    AUTHPASETO_TOKEN_LOCATION: set[str] = {"headers"}
    AUTHPASETO_DATABASE_URL: pydantic.RedisDsn
    EMAIL_CONFIRMATION_TOKEN_EXPIRES: datetime.timedelta = datetime.timedelta(days=7)
    RESET_PASSWORD_TOKEN_EXPIRES: datetime.timedelta = datetime.timedelta(hours=3)
    USER_PASSWORD_MIN_LENGTH: int = 8
    USER_PASSWORD_MAX_LENGTH: int = 32
    CONFIRM_EMAIL_URL: pydantic.AnyHttpUrl
    RESET_PASSWORD_URL: pydantic.AnyHttpUrl


class Database(pydantic.BaseSettings):
    DATABASE_URL: pydantic.PostgresDsn
    REDIS_URL: pydantic.RedisDsn


class Celery(pydantic.BaseSettings):
    CELERY_BROKER_URL: pydantic.RedisDsn
    CELERY_RESULT_BACKEND: pydantic.RedisDsn
    CELERY_ACCEPT_CONTENT: set[str] = {"application/json"}
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"


class Email(pydantic.BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_SENDER: pydantic.EmailStr


class Integration(pydantic.BaseSettings):
    SENTRY_DSN: str


class Settings(
    App, Security, Database, Celery, Email, Integration
):  # pylint: disable=too-many-ancestors
    class Config:
        case_sensitive = True


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
