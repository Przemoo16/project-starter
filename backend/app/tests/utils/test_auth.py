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
