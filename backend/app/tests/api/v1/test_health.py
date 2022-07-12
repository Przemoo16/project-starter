import typing

from fastapi import status
import pytest

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.anyio
async def test_check_health(async_client: "conftest.TestClient") -> None:
    response = await async_client.get(f"{API_URL}/health", follow_redirects=True)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
