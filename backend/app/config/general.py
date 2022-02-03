import functools
import logging
from typing import Any

import pydantic


class Settings(pydantic.BaseSettings):
    # App
    API_VERSION: str = "/api/v1"

    # Security
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
    LOGGING: dict[str, Any] = {
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


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()
