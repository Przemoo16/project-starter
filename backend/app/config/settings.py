import functools

import pydantic


class Settings(pydantic.BaseSettings):
    # Celery
    CELERY_BROKER_URL: pydantic.RedisDsn
    CELERY_RESULT_BACKEND: pydantic.RedisDsn
    CELERY_ACCEPT_CONTENT: set[str] = {"application/json"}
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()
