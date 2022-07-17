import typing

from fastapi import status
import fastapi_jwt_auth as jwt_auth
import pytest

from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.anyio
async def test_obtain_tokens(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    email = "test@email.com"
    await user_helpers.create_active_user(
        session=session,
        email=email,
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
    )
    request_data = {"username": email, "password": "plain_password"}

    response = await async_client.post(
        f"{API_URL}/token", data=request_data, follow_redirects=True
    )
    tokens = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "accessToken" in tokens
    assert "refreshToken" in tokens
    assert tokens["tokenType"] == "bearer"


@pytest.mark.anyio
async def test_refresh_token(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_active_user(session=session)
    token = jwt_auth.AuthJWT().create_refresh_token(str(user.id))
    request_data = {"token": token}

    response = await async_client.post(f"{API_URL}/token/refresh", json=request_data)
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "accessToken" in token
    assert token["tokenType"] == "bearer"


@pytest.mark.anyio
async def test_revoke_token(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(session=session)
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    request_data = {"token": token}

    response = await async_client.post(f"{API_URL}/token/revoke", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
