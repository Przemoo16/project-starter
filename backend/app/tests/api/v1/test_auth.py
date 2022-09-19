import typing
from unittest import mock

from fastapi import status
import fastapi_paseto_auth as paseto_auth
import pytest

from app.models import auth as auth_models

if typing.TYPE_CHECKING:
    from app.tests import conftest

API_URL = "/api/v1"


@pytest.mark.anyio
@mock.patch("app.services.auth.AuthService.obtain_tokens")
async def test_obtain_tokens(
    mock_obtain_tokens: mock.AsyncMock, async_client: "conftest.TestClient"
) -> None:
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    access_token = paseto_auth.AuthPASETO().create_access_token(user_id)
    refresh_token = paseto_auth.AuthPASETO().create_refresh_token(user_id)
    token_type = "bearer"
    mock_obtain_tokens.return_value = auth_models.AuthTokens(
        access_token=access_token, refresh_token=refresh_token, token_type=token_type
    )
    request_data = {"username": "test@email.com", "password": "plain_password"}

    response = await async_client.post(
        f"{API_URL}/token", data=request_data, follow_redirects=True
    )
    tokens = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert tokens["access_token"] == access_token
    assert tokens["refresh_token"] == refresh_token
    assert tokens["token_type"] == token_type


@pytest.mark.anyio
@mock.patch("app.services.auth.AuthService.refresh_token")
async def test_refresh_token(
    mock_refresh_token: mock.AsyncMock, async_client: "conftest.TestClient"
) -> None:
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    access_token = paseto_auth.AuthPASETO().create_access_token(user_id)
    token_type = "bearer"
    mock_refresh_token.return_value = auth_models.AccessToken(
        access_token=access_token, token_type=token_type
    )
    token = paseto_auth.AuthPASETO().create_refresh_token(user_id)
    request_data = {"token": token}

    response = await async_client.post(f"{API_URL}/token/refresh", json=request_data)
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert token["access_token"] == access_token
    assert token["token_type"] == token_type


@pytest.mark.anyio
@mock.patch("app.services.auth.AuthService.revoke_token", return_value=None)
async def test_revoke_token(
    _: mock.AsyncMock, async_client: "conftest.TestClient"
) -> None:
    user_id = "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    token = paseto_auth.AuthPASETO().create_access_token(user_id)
    request_data = {"token": token}

    response = await async_client.post(f"{API_URL}/token/revoke", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
