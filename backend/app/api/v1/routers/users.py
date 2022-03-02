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
    "/{user_id}",
    response_model=user_models.UserRead,
    responses={
        **user_exceptions.InactiveUserError().doc,
        **user_exceptions.UserForbiddenError().doc,
        **user_exceptions.UserNotFoundError().doc,
    },
)
async def get_user(
    user_id: user_models.UserID,
    current_user: user_models.User = fastapi.Depends(user_deps.get_current_active_user),
) -> typing.Any:
    await user_deps.check_user_requests_own_data(user_id, current_user)
    return current_user


@router.patch(
    "/{user_id}",
    response_model=user_models.UserRead,
    responses={
        **user_exceptions.InactiveUserError().doc,
        **user_exceptions.UserForbiddenError().doc,
        **user_exceptions.UserNotFoundError().doc,
    },
)
async def update_user(
    user_id: user_models.UserID,
    user: user_models.UserUpdateAPI,
    current_user: user_models.User = fastapi.Depends(user_deps.get_current_active_user),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    await user_deps.check_user_requests_own_data(user_id, current_user)
    return await user_services.UserService(session).update_user(
        current_user, user_models.UserUpdate(**user.dict(exclude_unset=True))
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **user_exceptions.InactiveUserError().doc,
        **user_exceptions.UserForbiddenError().doc,
        **user_exceptions.UserNotFoundError().doc,
    },
)
async def delete_user(
    user_id: user_models.UserID,
    Authorize: jwt_auth.AuthJWT = fastapi.Depends(),
    current_user: user_models.User = fastapi.Depends(user_deps.get_current_active_user),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    Authorize.fresh_jwt_required()
    await user_deps.check_user_requests_own_data(user_id, current_user)
    await user_services.UserService(session).delete_user(current_user)


@router.post(
    "/email-confirmation",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**user_exceptions.UserNotFoundError().doc},
)
async def confirm_email(
    key: user_models.UserConfirmationEmailKey = fastapi.Body(..., embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    user_db = await user_services.UserService(session).get_user(
        user_models.UserFilters(confirmation_email_key=key)
    )
    await user_services.UserService(session).confirm_email(user_db)


@router.post(
    "/password/reset-request",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=message.Message,
)
async def request_reset_password(
    email: user_models.UserEmail = fastapi.Body(..., embed=True),
    session: db.AsyncSession = fastapi.Depends(db.get_session),
) -> typing.Any:
    try:
        user_db = await user_services.UserService(session).get_user(
            user_models.UserFilters(email=email)
        )
    except user_exceptions.UserNotFoundError:
        log.info("Message has not been sent because user not found")
    else:
        user_services.UserService(session).request_reset_password(user_db)
    return message.Message(
        message="If provided valid email, the email to reset password has been sent"
    )


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
    user_db = await user_services.UserService(session).get_user(
        user_models.UserFilters(reset_password_key=key)
    )
    await user_services.UserService(session).reset_password(user_db, password)
