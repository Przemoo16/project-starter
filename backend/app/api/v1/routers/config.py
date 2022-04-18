import typing

import fastapi

from app.config import db
from app.models import config as config_models
from app.services import config as config_services

router = fastapi.APIRouter()


@router.get("/", response_model=config_models.Config)
async def get_config(
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return config_services.ConfigService(session).get_config()
