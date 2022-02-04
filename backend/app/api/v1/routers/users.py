from typing import Any

import fastapi
from fastapi import status

from app.api.deps import user as user_deps
from app.db import base
from app.models import user as user_model
from app.services import user as user_service

router = fastapi.APIRouter()


@router.post(
    "/", response_model=user_model.UserRead, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: user_model.UserCreate,
    session: base.AsyncSession = fastapi.Depends(base.get_session),
) -> Any:
    return await user_service.UserService(session).create_user(user)


@router.get(
    "/<user_id>",
    response_model=user_model.UserRead,
    status_code=status.HTTP_200_OK,
    dependencies=[fastapi.Depends(user_deps.check_user_requests_own_data)],
)
async def get_user(
    user_id: user_model.UserID,
    session: base.AsyncSession = fastapi.Depends(base.get_session),
) -> Any:
    return await user_service.UserService(session).get_user(user_id)


@router.patch(
    "/<user_id>",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[fastapi.Depends(user_deps.check_user_requests_own_data)],
)
async def update_user(
    user_id: user_model.UserID,
    user: user_model.UserUpdate,
    session: base.AsyncSession = fastapi.Depends(base.get_session),
) -> Any:
    await user_service.UserService(session).update_user(user_id, user)


@router.delete(
    "/<user_id>",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[fastapi.Depends(user_deps.check_user_requests_own_data)],
)
async def delete_user(
    user_id: user_model.UserID,
    session: base.AsyncSession = fastapi.Depends(base.get_session),
) -> Any:
    await user_service.UserService(session).delete_user(user_id)
