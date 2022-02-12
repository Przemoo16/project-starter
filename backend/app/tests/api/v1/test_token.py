import typing

from fastapi import status
import fastapi_jwt_auth as jwt_auth
import pytest

from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.asyncio
async def test_obtain_tokens(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    email = "test@example.com"
    await user_helpers.create_user(
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
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_token(
    async_client: "conftest.TestClient", session: "conftest.AsyncSession"
) -> None:
    user = await user_helpers.create_user(
        session=session, email="test@example.com", password="hashed_password"
    )
    token = jwt_auth.AuthJWT().create_refresh_token(str(user.id))
    request_data = {"token": token}

    response = await async_client.post(f"{API_URL}/token/refresh", json=request_data)
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in token
    assert token["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_revoke_token_token(async_client: "conftest.TestClient") -> None:
    user_id = "0dd53909-fcda-4c72-afcd-1bf4886389f8"
    token = jwt_auth.AuthJWT().create_refresh_token(user_id)
    request_data = {"token": token}

    response = await async_client.post(f"{API_URL}/token/revoke", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
