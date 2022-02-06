from jose import jwt

from app.config import general

settings = general.get_settings()


def is_token_fresh(token: str) -> bool:
    decoded_token = jwt.decode(
        token=token,
        key=settings.AUTHJWT_SECRET_KEY,
        algorithms=settings.AUTHJWT_DECODE_ALGORITHMS,
        options={"verify_exp": False},
    )
    return decoded_token["fresh"]
