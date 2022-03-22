import datetime
import functools

import pydantic


class App(pydantic.BaseSettings):
    APP_NAME: str = "Project starter"
    API_VERSION: str = "v1"
    LOCALES: list[str] = ["en"]
    API_URL: str = f"/api/{API_VERSION}"


class Security(pydantic.BaseSettings):
    SECRET_KEY: str
    TOKEN_URL: str = "/token"
    REFRESH_TOKEN_URL: str = f"/{TOKEN_URL}/refresh"
    AUTHJWT_SECRET_KEY: str
    AUTHJWT_ACCESS_TOKEN_EXPIRES: datetime.timedelta = datetime.timedelta(minutes=30)
    AUTHJWT_REFRESH_TOKEN_EXPIRES: datetime.timedelta = datetime.timedelta(days=1)
    AUTHJWT_DENYLIST_ENABLED: bool = True
    AUTHJWT_DENYLIST_TOKEN_CHECKS: set[str] = {"access", "refresh"}
    AUTHJWT_TOKEN_LOCATION: set[str] = {"headers"}
    AUTHJWT_ALGORITHM: str = "HS256"
    AUTHJWT_DECODE_ALGORITHMS: set[str] = {"HS256"}
    AUTHJWT_DATABASE_URL: pydantic.RedisDsn
    ACCOUNT_ACTIVATION_DAYS: int = 7
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
    EMAIL_SENDER_EMAIL: pydantic.EmailStr


class Settings(App, Security, Database, Celery, Email):
    class Config:
        case_sensitive = True


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()
