import typing
from unittest import mock

import pytest
from fastapi import status

from app.models import config as config_models
from app.tests.helpers import response as response_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.anyio
@mock.patch("app.services.config.get_config")
async def test_get_config(
    mock_get_config: mock.MagicMock, async_client: "conftest.TestClient"
) -> None:
    mock_get_config.return_value = config_models.Config(
        user_name_min_length=4,
        user_name_max_length=64,
        user_password_min_length=8,
        user_password_max_length=32,
    )

    response = await async_client.get(f"{API_URL}/config", follow_redirects=True)
    retrieved_config = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert retrieved_config == response_helpers.format_response(
        {
            "userNameMinLength": 4,
            "userNameMaxLength": 64,
            "userPasswordMinLength": 8,
            "userPasswordMaxLength": 32,
        }
    )
