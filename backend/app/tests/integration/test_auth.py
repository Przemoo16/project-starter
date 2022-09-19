import typing
from unittest import mock

import pytest

from app.config import general
from app.utils import converters

if typing.TYPE_CHECKING:
    from app.tests import conftest

settings = general.get_settings()

API_URL = settings.API_URL


@pytest.mark.anyio
async def test_auth_flow(async_client: "conftest.TestClient") -> None:
    # Create a user
    email = "test@email.com"
    password = "plain_password"
    email_confirmation_token = converters.to_uuid(
        "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    )
    with mock.patch("uuid.uuid4", return_value=email_confirmation_token):
        response = await async_client.post(
            f"{API_URL}/users",
            json={"email": email, "password": password, "name": "Test User"},
            follow_redirects=True,
        )

    assert response.status_code == 201

    # Confirm email
    response = await async_client.post(
        f"{API_URL}/users/email-confirmation",
        json={"token": str(email_confirmation_token)},
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


@pytest.mark.anyio
async def test_tokens_flow(async_client: "conftest.TestClient") -> None:
    # Create a user
    email = "test@email.com"
    password = "plain_password"
    email_confirmation_token = converters.to_uuid(
        "1dd53909-fcda-4c72-afcd-1bf4886389f8"
    )
    with mock.patch("uuid.uuid4", return_value=email_confirmation_token):
        response = await async_client.post(
            f"{API_URL}/users",
            json={"email": email, "password": password, "name": "Test User"},
            follow_redirects=True,
        )

    assert response.status_code == 201

    # Confirm email
    response = await async_client.post(
        f"{API_URL}/users/email-confirmation",
        json={"token": str(email_confirmation_token)},
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
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert "token_type" in tokens

    # Retrieve the user info
    access_token = tokens["access_token"]
    response = await async_client.get(
        f"{API_URL}/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    # Revoke access token
    response = await async_client.post(
        f"{API_URL}/token/revoke", json={"token": access_token}
    )

    assert response.status_code == 204

    # Retrieve the user info with revoked access token
    response = await async_client.get(
        f"{API_URL}/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 401

    # Refresh access token
    refresh_token = tokens["refresh_token"]
    response = await async_client.post(
        f"{API_URL}/token/refresh", json={"token": refresh_token}
    )
    token = response.json()

    assert response.status_code == 200
    assert "access_token" in token
    assert token["token_type"] == "bearer"

    # Retrieve the user info
    access_token = token["access_token"]
    response = await async_client.get(
        f"{API_URL}/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
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
