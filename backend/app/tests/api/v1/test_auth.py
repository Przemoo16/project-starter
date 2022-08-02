import typing
from unittest import mock

from fastapi import status
import fastapi_jwt_auth as jwt_auth
import pytest

from app.models import auth as auth_models
from app.tests.helpers import user as user_helpers

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.anyio
@mock.patch("app.services.auth.AuthService.obtain_tokens")
async def test_obtain_tokens(
    mock_obtain_tokens: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    email = "test@email.com"
    user = await user_helpers.create_active_user(
        session=session,
        email=email,
        password="$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q",
    )
    access_token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    refresh_token = jwt_auth.AuthJWT().create_refresh_token(str(user.id))
    token_type = "bearer"
    mock_obtain_tokens.return_value = auth_models.AuthTokens(
        access_token=access_token, refresh_token=refresh_token, token_type=token_type
    )
    request_data = {"username": email, "password": "plain_password"}

    response = await async_client.post(
        f"{API_URL}/token", data=request_data, follow_redirects=True
    )
    tokens = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert tokens["accessToken"] == access_token
    assert tokens["refreshToken"] == refresh_token
    assert tokens["tokenType"] == token_type


@pytest.mark.anyio
@mock.patch("app.services.auth.AuthService.refresh_token")
async def test_refresh_token(
    mock_refresh_token: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_active_user(session=session)
    access_token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    token_type = "bearer"
    mock_refresh_token.return_value = auth_models.AccessToken(
        access_token=access_token, token_type=token_type
    )
    token = jwt_auth.AuthJWT().create_refresh_token(str(user.id))
    request_data = {"token": token}

    response = await async_client.post(f"{API_URL}/token/refresh", json=request_data)
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert token["accessToken"] == access_token
    assert token["tokenType"] == token_type


@pytest.mark.anyio
@mock.patch("app.services.auth.AuthService.revoke_token", return_value=None)
async def test_revoke_token(
    _: mock.AsyncMock,
    async_client: "conftest.TestClient",
    session: "conftest.AsyncSession",
) -> None:
    user = await user_helpers.create_user(session=session)
    token = jwt_auth.AuthJWT().create_access_token(str(user.id))
    request_data = {"token": token}

    response = await async_client.post(f"{API_URL}/token/revoke", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
