import datetime
import functools
import logging
import typing

import pydantic


class Settings(pydantic.BaseSettings):
    # App
    APP_NAME: str = "Project starter"
    API_VERSION: str = "v1"
    LOCALES: list[str] = ["en"]

    # Urls
    API_URL: str = f"/api/{API_VERSION}"
    TOKEN_URL: str = "/token"
    REFRESH_TOKEN_URL: str = f"/{TOKEN_URL}/refresh"
    FRONTEND_CONFIRM_EMAIL_URL: pydantic.AnyHttpUrl
    FRONTEND_RESET_PASSWORD_URL: pydantic.AnyHttpUrl

    # Security
    SECRET_KEY: str
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
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 32

    # Database
    DATABASE_URL: str
    REDIS_URL: str

    # Celery
    CELERY_BROKER_URL: pydantic.RedisDsn
    CELERY_RESULT_BACKEND: pydantic.RedisDsn
    CELERY_ACCEPT_CONTENT: set[str] = {"application/json"}
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"

    # Email
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_SENDER_EMAIL: pydantic.EmailStr

    # Logging
    LOGGING: dict[str, typing.Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(levelname)s: %(message)s"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": logging.DEBUG,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": logging.DEBUG,
        },
    }

    class Config:
        case_sensitive = True


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()
