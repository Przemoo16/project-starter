import typing
from unittest import mock

import pytest
from fastapi import status

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.anyio
@mock.patch("app.services.health.HealthService.check_health", return_value=None)
async def test_check_health(
    _: mock.AsyncMock, async_client: "conftest.TestClient"
) -> None:
    response = await async_client.get(f"{API_URL}/health", follow_redirects=True)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
