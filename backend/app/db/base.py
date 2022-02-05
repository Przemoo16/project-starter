import typing

from sqlalchemy import orm
from sqlalchemy.ext import asyncio

from app.config import general

settings = general.get_settings()

engine = asyncio.create_async_engine(settings.DATABASE_URL)

AsyncSession = asyncio.AsyncSession


async def get_session() -> typing.AsyncGenerator[
    AsyncSession, None
]:  # pragma: no cover
    async_session = orm.sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
