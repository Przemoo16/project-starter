import datetime

from passlib import context

pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_remaining_expiration(exp: int) -> int:
    delta = int(exp - datetime.datetime.utcnow().timestamp())
    return max(0, delta)
