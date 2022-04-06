import celery

from app.config import general
from app.utils import sentry

APPS = ["app"]

settings = general.get_settings()

sentry.init_sentry(settings.SENTRY_DSN, settings.DEV_MODE)

app = celery.Celery(
    "celery",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
)
app.autodiscover_tasks(packages=APPS)
