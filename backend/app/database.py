from typing import AsyncGenerator

from sqlalchemy import orm
from sqlalchemy.ext import asyncio

from app.config import general

settings = general.get_settings()

engine = asyncio.create_async_engine(settings.DATABASE_URL)


async def get_session() -> AsyncGenerator[asyncio.AsyncSession, None]:
    async_session = orm.sessionmaker(
        engine, class_=asyncio.AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
