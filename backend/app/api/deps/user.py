import logging

import fastapi
import fastapi_jwt_auth as jwt_auth
from sqlalchemy import exc

from app.db import base
from app.models import user as user_model
from app.services import auth, exceptions
from app.services import user as user_service
from app.utils import converters

log = logging.getLogger(__name__)


async def get_current_user(
    session: base.AsyncSession = fastapi.Depends(base.get_session),
    Authorize: jwt_auth.AuthJWT = fastapi.Depends(),
    token: str = fastapi.Depends(auth.oauth2_scheme),  # pylint: disable=unused-argument
) -> user_model.User:
    """
    Get current user.

    # oauth2_scheme dependency is only there to ensure the API documentation gets
    # generated correctly.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    if not user_id:
        log.info("User ID not found in the JWT subject")
        raise exceptions.UnauthorizedError()
    try:
        return await user_service.UserCRUD(session).read(
            id=converters.change_to_uuid(str(user_id))
        )
    except exc.NoResultFound as e:
        log.info("User with ID %r not found in the database", user_id)
        raise exceptions.UnauthorizedError() from e


async def get_current_active_user(
    user: user_model.User = fastapi.Depends(get_current_user),
) -> user_model.User:
    if not user.is_active:
        log.info("User with ID %r is not active", user.id)
        raise exceptions.ForbiddenError(context={"user": user.email})
    return user


async def check_user_requests_own_data(
    user_id: user_model.UserID,
    user: user_model.User = fastapi.Depends(get_current_active_user),
) -> None:
    if user_id == user.id:
        return
    log.info(
        "User with ID %r is not allowed to access data of user with ID %r",
        user.id,
        user_id,
    )
    raise exceptions.ForbiddenError({"id": user_id})
