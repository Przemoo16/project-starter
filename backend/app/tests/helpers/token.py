import typing

from jose import jwt

from app.config import general

settings = general.get_settings()


def decode_token(
    token: str, options: dict[str, typing.Any] | None = None
) -> dict[str, typing.Any]:
    return dict(
        jwt.decode(
            token=token,
            key=settings.AUTHJWT_SECRET_KEY,
            algorithms=settings.AUTHJWT_DECODE_ALGORITHMS,
            options=options,
        )
    )


def is_token_fresh(token: str) -> bool:
    decoded_token = decode_token(token=token, options={"verify_exp": False})
    return decoded_token["fresh"]
