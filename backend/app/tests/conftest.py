import typing

import httpx
import pytest
import pytest_asyncio
import redis
from sqlalchemy import orm
from sqlalchemy.ext import asyncio
import sqlmodel

from app import (  # noqa: F401 # pylint: disable=unused-import # Detect all models
    main,
    models,
)
from app.celery import worker
from app.config import db, general
from app.tests.mocks import email

AsyncSession: typing.TypeAlias = asyncio.AsyncSession
TestClient: typing.TypeAlias = httpx.AsyncClient
RedisClient: typing.TypeAlias = redis.Redis

settings = general.get_settings()

# Mocking SMTP works only in the app container, Celery still uses the original code
email.mock_smtp()


@pytest.fixture(name="redis_client", scope="session")
def redis_client_fixture() -> typing.Generator[RedisClient, None, None]:
    yield redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


@pytest.fixture(name="flush_redis")
def flush_redis_fixture(
    redis_client: RedisClient,
) -> typing.Generator[None, None, None]:
    yield
    redis_client.flushall()


@pytest.fixture(name="purge_celery")
def purge_celery_fixture() -> typing.Generator[None, None, None]:
    yield
    worker.app.control.purge()


@pytest.fixture(name="engine")  # TODO: Use one connection in the whole session
def engine_fixture() -> typing.Generator[asyncio.AsyncEngine, None, None]:
    yield asyncio.create_async_engine(settings.DATABASE_URL)


@pytest_asyncio.fixture(name="create_tables")
async def create_tables_fixture(
    engine: asyncio.AsyncEngine,
) -> typing.AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(sqlmodel.SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(name="session")
async def session_fixture(
    engine: asyncio.AsyncEngine,
    create_tables: None,  # pylint: disable=unused-argument
    purge_celery: None,  # pylint: disable=unused-argument
    flush_redis: None,  # pylint: disable=unused-argument
) -> typing.AsyncGenerator[AsyncSession, None]:
    async_session = orm.sessionmaker(
        engine, class_=asyncio.AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(name="async_client")
async def async_client_fixture(
    session: AsyncSession,
) -> typing.AsyncGenerator[TestClient, None]:
    main.app.dependency_overrides[db.get_session] = lambda: session
    async with httpx.AsyncClient(app=main.app, base_url="http://test") as client:
        yield client
    main.app.dependency_overrides.clear()
