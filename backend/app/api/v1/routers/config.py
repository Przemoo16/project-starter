import typing

import fastapi

from app.models import config as config_models
from app.services import config as config_services

router = fastapi.APIRouter()


@router.get("/", response_model=config_models.Config)
async def get_config() -> typing.Any:
    return config_services.get_config()
