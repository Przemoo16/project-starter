import logging
import typing

import fastapi
from fastapi import status
import fastapi_jwt_auth as jwt_auth

from app.api.deps import user as user_deps
from app.config import db, general
from app.exceptions.http import user as user_exceptions
from app.models import message
from app.models import user as user_models
from app.services import user as user_services

settings = general.get_settings()

router = fastapi.APIRouter()

log = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=user_models.UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={**user_exceptions.UserAlreadyExistsError().doc},
)
async def create_user(
    user: user_models.UserCreate,
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return await user_services.UserService(session).create_user(user)


@router.get(
    "/me",
    response_model=user_models.UserRead,
    responses=user_deps.INACTIVE_USER_RESPONSES,
)
async def get_me(
    current_user: user_models.User = fastapi.Depends(user_deps.get_current_active_user),
) -> typing.Any:
    return current_user


@router.patch(
    "/me",
    response_model=user_models.UserRead,
    responses=user_deps.INACTIVE_USER_RESPONSES,
)
async def update_me(
    user: user_models.UserUpdateAPI,
    current_user: user_models.User = fastapi.Depends(user_deps.get_current_active_user),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return await user_services.UserService(session).update_user(
        current_user, user_models.UserUpdate(**user.dict(exclude_unset=True))
    )


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=user_deps.INACTIVE_USER_RESPONSES,
)
async def delete_me(
    Authorize: jwt_auth.AuthJWT = fastapi.Depends(),
    current_user: user_models.User = fastapi.Depends(user_deps.get_current_active_user),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    Authorize.fresh_jwt_required()
    await user_services.UserService(session).delete_user(current_user)


@router.get(
    "/{user_id}",
    response_model=user_models.UserRead,
    dependencies=[fastapi.Depends(user_deps.get_current_active_user)],
    responses=user_deps.INACTIVE_USER_RESPONSES,
)
async def get_user(
    user_id: user_models.UserID,
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    return await user_services.UserService(session).get_user(
        user_models.UserFilters(id=user_id)
    )


@router.post(
    "/email-confirmation",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **user_exceptions.UserNotFoundError().doc,
        **user_exceptions.ConfirmationEmailError().doc,
    },
)
async def confirm_email(
    key: user_models.UserConfirmationEmailKey = fastapi.Body(..., embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    user_service = user_services.UserService(session)
    user_db = await user_service.get_user(
        user_models.UserFilters(confirmation_email_key=key)
    )
    await user_service.confirm_email(user_db)


@router.post(
    "/password/reset-request",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=message.Message,
)
async def request_reset_password(
    email: user_models.UserEmail = fastapi.Body(..., embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    user_service = user_services.UserService(session)
    try:
        user_db = await user_service.get_user(user_models.UserFilters(email=email))
    except user_exceptions.UserNotFoundError:
        log.info("Message has not been sent because user not found")
    else:
        user_service.request_reset_password(user_db)
    return {
        "message": "If provided valid email, the email to reset password has been sent"
    }


@router.post(
    "/password/reset",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**user_exceptions.UserNotFoundError().doc},
)
async def reset_password(
    key: user_models.UserResetPasswordKey = fastapi.Body(..., embed=True),
    password: user_models.UserPassword = fastapi.Body(..., embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    user_service = user_services.UserService(session)
    user_db = await user_service.get_user(
        user_models.UserFilters(reset_password_key=key)
    )
    await user_service.reset_password(user_db, password)
