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
