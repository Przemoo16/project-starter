import datetime
import typing
from unittest import mock

import freezegun
import pytest

from app.models import reset_password as reset_password_models
from app.tests.helpers import db
from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.anyio
@freezegun.freeze_time("2023-07-16 16:00:00")
@mock.patch(
    "app.services.user.settings.RESET_PASSWORD_TOKEN_EXPIRES",
    new=datetime.timedelta(minutes=30),
)
async def test_reset_password_token_model(session: "conftest.AsyncSession") -> None:
    user = await user_helpers.create_user(session)
    token = reset_password_models.ResetPasswordToken(user=user)

    await db.save(session, token)

    assert token.id
    assert token.expire_at == datetime.datetime(
        2023, 7, 16, 16, 0, 0
    ) + datetime.timedelta(minutes=30)
    assert token.created_at == datetime.datetime(2023, 7, 16, 16, 0, 0)
    assert token.updated_at == datetime.datetime(2023, 7, 16, 16, 0, 0)
    assert token.user_id == user.id
    assert token.user == user
    assert token.is_expired is False
