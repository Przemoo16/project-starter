from logging import config

import fastapi

from app.api.v1 import api
from app.config import general
from app.exceptions import handlers
from app.utils import openapi, responses

settings = general.get_settings()
config.fileConfig("logging.conf", disable_existing_loggers=False)

app = fastapi.FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_URL}/openapi.json",
    default_response_class=responses.ORJSONResponse,
)

handlers.init_handlers(app)

app.include_router(api.router, prefix=settings.API_URL)

app.openapi = openapi.generate_openapi_schema(app)
