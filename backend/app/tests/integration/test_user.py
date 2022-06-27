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
async def test_confirm_email_flow(async_client: "conftest.TestClient") -> None:
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

    # Authorize the user
    response = await async_client.post(
        f"{API_URL}/token",
        data={"username": email, "password": password},
        follow_redirects=True,
    )

    assert response.status_code == 403

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

    assert response.status_code == 200


@pytest.mark.anyio
async def test_change_password_flow(async_client: "conftest.TestClient") -> None:
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

    # Change the user password
    new_password = "new_password"
    access_token = tokens["accessToken"]
    response = await async_client.post(
        f"{API_URL}/users/me/password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"oldPassword": password, "newPassword": new_password},
    )

    assert response.status_code == 204

    # Authorize the user with the old password
    response = await async_client.post(
        f"{API_URL}/token",
        data={"username": email, "password": password},
        follow_redirects=True,
    )

    assert response.status_code == 401

    # Authorize the user with the new password
    response = await async_client.post(
        f"{API_URL}/token",
        data={"username": email, "password": new_password},
        follow_redirects=True,
    )

    assert response.status_code == 200


@pytest.mark.anyio
async def test_reset_password_flow(async_client: "conftest.TestClient") -> None:
    # Create a user
    email = "test@email.com"
    password = "plain_password"
    reset_password_key = converters.to_uuid("1dd53909-fcda-4c72-afcd-1bf4886389f8")
    confirmation_email_key = reset_password_key
    with mock.patch("uuid.uuid4", return_value=reset_password_key):
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

    # Reset password
    response = await async_client.post(
        f"{API_URL}/users/password/reset",
        json={"email": email},
    )

    assert response.status_code == 202

    # Set new password
    new_password = "new_password"
    response = await async_client.post(
        f"{API_URL}/users/password/set",
        json={"key": str(reset_password_key), "password": new_password},
    )

    assert response.status_code == 204

    # Authorize the user
    response = await async_client.post(
        f"{API_URL}/token",
        data={"username": email, "password": new_password},
        follow_redirects=True,
    )

    assert response.status_code == 200
