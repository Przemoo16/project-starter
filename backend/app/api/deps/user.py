import logging

import fastapi
import fastapi_jwt_auth as jwt_auth
from sqlalchemy import exc

from app.config import db
from app.exceptions import resource
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
        raise resource.UnauthorizedError()
    try:
        return await user_services.UserCRUD(session).read(
            id=converters.change_to_uuid(str(user_id))
        )
    except exc.NoResultFound as e:
        log.info("User with ID %r not found in the database", user_id)
        raise resource.UnauthorizedError() from e


async def get_current_active_user(
    user: user_models.User = fastapi.Depends(get_current_user),
) -> user_models.User:
    if not user.is_active:
        log.info("User with ID %r is not active", user.id)
        raise resource.ForbiddenError(context={"user": user.email})
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
    raise resource.ForbiddenError({"id": user_id})
