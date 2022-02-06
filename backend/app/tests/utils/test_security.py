import datetime

import freezegun

from app.utils import security


def test_hash_password() -> None:
    password = "plain_password"

    hashed_password = security.hash_password(password)

    assert hashed_password != password


def test_verify_password() -> None:
    password = "plain_password"
    hashed_password = "$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42q"

    verified_password = security.verify_password(password, hashed_password)

    assert verified_password is True


def test_verify_password_wrong_password() -> None:
    password = "plain_password"
    hashed_password = "$2b$12$q8JcpltDZkSLOdMuPyt/jORzExLKp9HsKgCoFJQ1IzzITc2/Pg42Q"

    verified_password = security.verify_password(password, hashed_password)

    assert verified_password is False


@freezegun.freeze_time("2022-02-06 12:30:00")
def test_get_remaining_expiration() -> None:
    exp = int(datetime.datetime(2022, 2, 6, 13, 0, 0).timestamp())

    remaining_expiration = security.get_remaining_expiration(exp)

    assert remaining_expiration == 1800


@freezegun.freeze_time("2022-02-06 12:30:00")
def test_get_remaining_expiration_already_expired() -> None:
    exp = int(datetime.datetime(2022, 2, 6, 12, 0, 0).timestamp())

    remaining_expiration = security.get_remaining_expiration(exp)

    assert remaining_expiration == 0
