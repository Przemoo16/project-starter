import datetime
import functools
import logging
import typing

import pydantic


class Settings(pydantic.BaseSettings):
    # App
    API_VERSION: str = "/api/v1"

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
    ACCOUNT_ACTIVATION_DAYS = 7

    # Database
    DATABASE_URL: str

    # Celery
    CELERY_BROKER_URL: pydantic.RedisDsn
    CELERY_RESULT_BACKEND: pydantic.RedisDsn
    CELERY_ACCEPT_CONTENT: set[str] = {"application/json"}
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"

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
