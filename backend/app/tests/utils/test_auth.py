import fastapi_paseto_auth as paseto_auth
import pytest

from app.exceptions.app import auth as auth_exceptions
from app.utils import auth


def test_hash_password() -> None:
    password = "plain_password"

    hashed_password = auth.hash_password(password)

    assert hashed_password != password


def test_verify_password() -> None:
    password = "plain_password"
    hashed_password = (
        "$argon2id$v=19$m=65536,t=3,p=4$AoDw3nvPea/VGiNkzPn/Pw$grh02g7mdXN47S8kSt2P"
        "Vmv52AAt7wisY63TPS80qMo"
    )

    verified_password = auth.verify_password(password, hashed_password)

    assert verified_password is True


def test_verify_password_wrong_password() -> None:
    password = "plain_password"
    hashed_password = (
        "$argon2id$v=19$m=65536,t=3,p=4$sDZmjFEq5byXUsq5FwJgjA$ZrdX+g7VI+EYyTWlgrvNiD30"
        "VeOvQYJIcJAz04MbVe0"
    )

    verified_password = auth.verify_password(password, hashed_password)

    assert verified_password is False


def test_decode_token() -> None:
    subject = "test-subject"
    token = paseto_auth.AuthPASETO().create_access_token(subject)

    decoded_token = auth.decode_token(token)

    assert isinstance(decoded_token.payload, dict)
    assert decoded_token.payload["sub"] == subject


def test_decode_token_error() -> None:
    with pytest.raises(auth_exceptions.TokenDecodingError):
        auth.decode_token("invalid_token")


def test_decode_token_payload() -> None:
    subject = "test-subject"
    token = paseto_auth.AuthPASETO().create_access_token(subject)

    payload = auth.decode_token_payload(token)

    assert payload["sub"] == subject


def test_is_token_fresh() -> None:
    token = paseto_auth.AuthPASETO().create_access_token("payload", fresh=True)

    fresh = auth.is_token_fresh(token)

    assert fresh


def test_is_token_fresh_no_fresh() -> None:
    token = paseto_auth.AuthPASETO().create_access_token("payload")

    fresh = auth.is_token_fresh(token)

    assert not fresh
