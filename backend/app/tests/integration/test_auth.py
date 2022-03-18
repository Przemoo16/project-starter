import typing
from unittest import mock

import pytest

from app.config import general
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest

settings = general.get_settings()

API_URL = settings.API_URL


@pytest.mark.asyncio
async def test_auth_flow(async_client: "conftest.TestClient") -> None:
    # Create a user
    email = "test@email.com"
    password = "plain_password"
    confirmation_email_key = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    with mock.patch("uuid.uuid4", return_value=confirmation_email_key):
        response = await async_client.post(
            f"{API_URL}/users",
            json={"email": email, "password": password, "name": "Test User"},
            follow_redirects=True,
        )

    assert response.status_code == 201

    # Confirm email
    response = await async_client.post(
        f"{API_URL}/users/email-confirmation",
        json={"key": str(confirmation_email_key)},
    )

    # Auth with wrong email
    response = await async_client.post(
        f"{API_URL}/token",
        data={"username": "invalid@email.com", "password": password},
        follow_redirects=True,
    )

    assert response.status_code == 401

    # Auth with wrong password
    response = await async_client.post(
        f"{API_URL}/token",
        data={"username": email, "password": "invalid_password"},
        follow_redirects=True,
    )

    assert response.status_code == 401

    # Auth with valid credentials
    response = await async_client.post(
        f"{API_URL}/token",
        data={"username": email, "password": password},
        follow_redirects=True,
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_tokens_flow(async_client: "conftest.TestClient") -> None:
    # Create a user
    email = "test@email.com"
    password = "plain_password"
    confirmation_email_key = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    with mock.patch("uuid.uuid4", return_value=confirmation_email_key):
        response = await async_client.post(
            f"{API_URL}/users",
            json={"email": email, "password": password, "name": "Test User"},
            follow_redirects=True,
        )

    assert response.status_code == 201

    # Confirm email
    response = await async_client.post(
        f"{API_URL}/users/email-confirmation",
        json={"key": str(confirmation_email_key)},
    )

    assert response.status_code == 204

    # Authorize the user
    response = await async_client.post(
        f"{API_URL}/token",
        data={"username": email, "password": password},
        follow_redirects=True,
    )
    tokens = response.json()

    assert response.status_code == 200
    assert "accessToken" in tokens
    assert "refreshToken" in tokens
    assert "tokenType" in tokens

    # Update the user password
    access_token = tokens["accessToken"]
    response = await async_client.patch(
        f"{API_URL}/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"password": "new_password"},
    )

    assert response.status_code == 200

    # Revoke access token
    response = await async_client.post(
        f"{API_URL}/token/revoke", json={"token": access_token}
    )

    assert response.status_code == 204

    # Update the user password with revoked access token
    response = await async_client.patch(
        f"{API_URL}/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"password": "another_new_password"},
    )

    assert response.status_code == 401

    # Refresh access token
    refresh_token = tokens["refreshToken"]
    response = await async_client.post(
        f"{API_URL}/token/refresh", json={"token": refresh_token}
    )
    token = response.json()

    assert response.status_code == 200
    assert "accessToken" in token
    assert token["tokenType"] == "bearer"

    # Update the user password
    access_token = token["accessToken"]
    response = await async_client.patch(
        f"{API_URL}/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"password": "another_new_password"},
    )

    assert response.status_code == 200

    # Revoke refresh token
    response = await async_client.post(
        f"{API_URL}/token/revoke", json={"token": refresh_token}
    )

    assert response.status_code == 204

    # Refresh access token with revoked refresh token
    token_response = await async_client.post(
        f"{API_URL}/token/refresh", json={"token": refresh_token}
    )

    assert token_response.status_code == 401
