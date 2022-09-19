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
        json={"token": str(email_confirmation_token)},
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

    # Change the user password
    new_password = "new_password"
    access_token = tokens["access_token"]
    response = await async_client.post(
        f"{API_URL}/users/me/password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"currentPassword": password, "newPassword": new_password},
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

    # Reset password generate first token
    reset_password_token_1 = converters.to_uuid("3c1cf7f7-33cd-492f-b9b1-75bebf2752d1")
    with mock.patch("uuid.uuid4", return_value=reset_password_token_1):
        response = await async_client.post(
            f"{API_URL}/users/password/reset",
            json={"email": email},
        )

    assert response.status_code == 202

    # Reset password generate second token
    reset_password_token_2 = converters.to_uuid("858de17d-2e7c-4728-9870-ee5d986debba")
    with mock.patch("uuid.uuid4", return_value=reset_password_token_2):
        response = await async_client.post(
            f"{API_URL}/users/password/reset",
            json={"email": email},
        )

    assert response.status_code == 202

    # Set new password with first token
    new_password_first_token = "new_password_first_token"
    response = await async_client.post(
        f"{API_URL}/users/password/set",
        json={
            "token": str(reset_password_token_1),
            "password": new_password_first_token,
        },
    )

    assert response.status_code == 422

    # Set new password with second token
    new_password_second_token = "new_password_second_token"
    response = await async_client.post(
        f"{API_URL}/users/password/set",
        json={
            "token": str(reset_password_token_2),
            "password": new_password_second_token,
        },
    )

    assert response.status_code == 204

    # Authorize the user
    response = await async_client.post(
        f"{API_URL}/token",
        data={"username": email, "password": new_password_second_token},
        follow_redirects=True,
    )

    assert response.status_code == 200

    # Set new password with already used token
    another_new_password = "another_new_password"
    response = await async_client.post(
        f"{API_URL}/users/password/set",
        json={"token": str(reset_password_token_2), "password": another_new_password},
    )

    assert response.status_code == 422
