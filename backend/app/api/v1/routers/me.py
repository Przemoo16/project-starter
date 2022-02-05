from typing import Any

import fastapi
from fastapi import status

from app.api.deps import user as user_deps
from app.db import base
from app.models import user as user_model
from app.services import user as user_services

router = fastapi.APIRouter()


@router.get(
    "/",
    response_model=user_model.UserRead,
    status_code=status.HTTP_200_OK,
)
async def me(
    current_user: user_model.User = fastapi.Depends(user_deps.get_current_active_user),
) -> Any:
    return current_user


@router.put("/email", status_code=status.HTTP_204_NO_CONTENT)
async def confirm_email(
    confirmation_email: user_model.ConfirmationEmail,
    session: base.AsyncSession = fastapi.Depends(base.get_session),
) -> Any:
    await user_services.UserService(session).confirm_email(confirmation_email.key)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password() -> Any:
    pass


@router.post("/password/request-reset", status_code=status.HTTP_204_NO_CONTENT)
async def request_reset_password() -> Any:
    pass


@router.put("/password/reset", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password() -> Any:
    pass
