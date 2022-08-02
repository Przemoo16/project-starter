import typing

import fastapi
from fastapi import status

from app.config import db
from app.exceptions.http import health as health_exceptions
from app.services import health as health_services

router = fastapi.APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**health_exceptions.HealthError().doc},
)
async def check_health(
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    await health_services.HealthService(session).check_health()
