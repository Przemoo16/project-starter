from logging import config

import fastapi

from app.api.v1 import api
from app.config import general
from app.exceptions import handlers
from app.utils import openapi, responses, sentry

settings = general.get_settings()

config.fileConfig("logging.conf", disable_existing_loggers=False)

app = fastapi.FastAPI(
    title=settings.APP_NAME,
    default_response_class=responses.ORJSONResponse,
    openapi_url="/openapi.json" if settings.DEV_MODE else None,
    docs_url="/docs" if settings.DEV_MODE else None,
    redoc_url="/redoc" if settings.DEV_MODE else None,
)

sentry.init_sentry(settings.SENTRY_DSN, settings.DEV_MODE)

handlers.init_handlers(app)

app.include_router(api.router, prefix=settings.API_URL)

app.openapi = openapi.generate_openapi_schema(app)  # type: ignore
