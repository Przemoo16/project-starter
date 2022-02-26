import logging

import fastapi
import fastapi_jwt_auth as jwt_auth

from app.config import db
from app.exceptions.http import user as user_exceptions
from app.models import user as user_models
from app.services import auth
from app.services import user as user_services
from app.utils import converters

log = logging.getLogger(__name__)


async def get_current_user(
    session: db.AsyncSession = fastapi.Depends(db.get_session),
    Authorize: jwt_auth.AuthJWT = fastapi.Depends(),
    token: str = fastapi.Depends(auth.oauth2_scheme),  # pylint: disable=unused-argument
) -> user_models.User:
    """
    Get current user.

    # oauth2_scheme dependency is only there to ensure the API documentation gets
    # generated correctly.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    if not user_id:
        log.info("User ID not found in the JWT subject")
        raise user_exceptions.UnauthorizedUserError()
    user_filters = user_models.UserFilters(id=converters.to_uuid(str(user_id)))
    try:
        return await user_services.UserService(session).get_user(user_filters)
    except user_exceptions.UserNotFoundError as e:
        log.info("User with ID %r not found in the database", user_id)
        raise user_exceptions.UnauthorizedUserError(context={"id": user_id}) from e


async def get_current_active_user(
    user: user_models.User = fastapi.Depends(get_current_user),
) -> user_models.User:
    if not user.is_active:
        raise user_exceptions.InactiveUserError(context={"id": user.id})
    return user


async def check_user_requests_own_data(
    user_id: user_models.UserID,
    user: user_models.User = fastapi.Depends(get_current_active_user),
) -> None:
    if user_id == user.id:
        return
    log.info(
        "User with ID %r is not allowed to access data of user with ID %r",
        user.id,
        user_id,
    )
    raise user_exceptions.UserForbiddenError(context={"id": user_id})
