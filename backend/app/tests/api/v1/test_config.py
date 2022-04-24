import typing

from fastapi import status
import pytest

from app.tests.helpers import response as response_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.asyncio
async def test_get_config(
    async_client: "conftest.TestClient",
    mock_common: None,  # pylint: disable=unused-argument
) -> None:
    response = await async_client.get(f"{API_URL}/config", follow_redirects=True)
    retrieved_config = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert retrieved_config == response_helpers.format_response(
        {
            "appName": "Project Starter",
            "userNameMaxLength": 64,
            "userPasswordMinLength": 8,
            "userPasswordMaxLength": 32,
        }
    )
