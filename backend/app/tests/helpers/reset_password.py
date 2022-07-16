import typing

from app.models import reset_password
from app.tests.helpers import db
from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest


async def create_reset_password_token(
    session: "conftest.AsyncSession", **kwargs: typing.Any
) -> reset_password.ResetPasswordToken:
    if "user_id" not in kwargs and "user" not in kwargs:
        kwargs["user"] = await user_helpers.create_active_user(session)
    token = reset_password.ResetPasswordToken(**kwargs)
    return await db.save(session, token)
