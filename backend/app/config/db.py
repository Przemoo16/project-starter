import functools
import typing

import redis
from sqlalchemy import orm
from sqlalchemy.ext import asyncio

from app.config import general

AsyncSession: typing.TypeAlias = asyncio.AsyncSession

settings = general.get_settings()

engine = asyncio.create_async_engine(settings.DATABASE_URL)

# TODO: Change to AsyncSession from the SQLModel when
# https://github.com/tiangolo/sqlmodel/issues/54 will be resolved.
# Then replace session.execute with session.exec in the whole codebase.
session_factory = orm.sessionmaker(
    engine, class_=asyncio.AsyncSession, expire_on_commit=False
)


async def get_session() -> typing.AsyncGenerator[
    AsyncSession, None
]:  # pragma: no cover
    async with session_factory() as session:
        yield session


@functools.lru_cache
def get_paseto_token_db() -> redis.Redis:  # type: ignore
    return redis.Redis.from_url(settings.AUTHPASETO_DATABASE_URL, decode_responses=True)
