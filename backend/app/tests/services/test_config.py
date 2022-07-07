import typing
from unittest import mock

import pytest

from app.models import config as config_models
from app.services import config as config_services

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.anyio
@mock.patch("app.models.user.USER_NAME_MIN_LENGTH", new=4)
@mock.patch("app.models.user.USER_NAME_MAX_LENGTH", new=64)
@mock.patch("app.services.config.settings.USER_PASSWORD_MIN_LENGTH", new=8)
@mock.patch("app.services.config.settings.USER_PASSWORD_MAX_LENGTH", new=32)
async def test_config_service_get_config(session: "conftest.AsyncSession") -> None:
    config = config_services.ConfigService(session).get_config()

    assert config == config_models.Config(
        user_name_min_length=4,
        user_name_max_length=64,
        user_password_min_length=8,
        user_password_max_length=32,
    )
