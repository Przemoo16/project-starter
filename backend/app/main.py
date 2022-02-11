import fastapi

from app.api.v1 import api
from app.config import general
from app.exceptions import handlers
from app.utils import openapi

settings = general.get_settings()

app = fastapi.FastAPI(
    title=settings.APP_NAME, openapi_url=f"{settings.API_URL}/openapi.json"
)

handlers.init_handlers(app)

app.include_router(api.router, prefix=settings.API_URL)

app.openapi = openapi.generate_openapi_schema(app)
