from celery import Celery

from app.config.settings import get_settings

APPS = ["app"]

settings = get_settings()

app = Celery(
    "celery",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
)
app.autodiscover_tasks(packages=APPS)
