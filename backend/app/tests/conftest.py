import typing

import httpx
import pytest
import redis
from sqlalchemy import orm
from sqlalchemy.ext import asyncio
import sqlmodel

from app import main
from app.celery import worker
from app.config import db, general
from app.tests.mocks import email as email_mocks

if typing.TYPE_CHECKING:
    from _pytest import monkeypatch as pytest_monkeypatch


AsyncSession: typing.TypeAlias = asyncio.AsyncSession
TestClient: typing.TypeAlias = httpx.AsyncClient
RedisClient: typing.TypeAlias = redis.Redis

settings = general.get_settings()


@pytest.fixture(name="anyio_backend", scope="session")
def anyio_backend_fixture() -> str:
    return "asyncio"


@pytest.fixture(name="redis_client", scope="session")
def redis_client_fixture() -> typing.Generator[RedisClient, None, None]:  # type: ignore
    yield redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


@pytest.fixture(name="flush_redis")
def flush_redis_fixture(
    redis_client: RedisClient,  # type: ignore
) -> typing.Generator[None, None, None]:
    yield
    redis_client.flushall()


@pytest.fixture(name="purge_celery")
def purge_celery_fixture() -> typing.Generator[None, None, None]:
    yield
    worker.app.control.purge()


# TODO: Use one engine in the whole session. The connection cannot be shared by
# many requests: "cannot perform operation: another operation is in progress"
@pytest.fixture(name="engine")
def engine_fixture() -> typing.Generator[asyncio.AsyncEngine, None, None]:
    yield asyncio.create_async_engine(settings.DATABASE_URL)


@pytest.fixture(name="create_tables")
async def create_tables_fixture(
    engine: asyncio.AsyncEngine,
) -> typing.AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(sqlmodel.SQLModel.metadata.drop_all)


@pytest.fixture(name="session")
async def session_fixture(  # pylint: disable=unused-argument
    engine: asyncio.AsyncEngine,
    create_tables: None,
    purge_celery: None,
    flush_redis: None,
) -> typing.AsyncGenerator[AsyncSession, None]:
    async_session = orm.sessionmaker(
        engine, class_=asyncio.AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture(name="async_client")
async def async_client_fixture(
    session: AsyncSession,
) -> typing.AsyncGenerator[TestClient, None]:
    main.app.dependency_overrides[db.get_session] = lambda: session
    async with httpx.AsyncClient(app=main.app, base_url="http://test") as client:
        yield client
    main.app.dependency_overrides.clear()


@pytest.fixture(name="mock_common", autouse=True)
def mock_common_fixture(monkeypatch: "pytest_monkeypatch.MonkeyPatch") -> None:
    monkeypatch.setattr("smtplib.SMTP", email_mocks.MockSMTP)
    monkeypatch.setattr("smtplib.SMTP_SSL", email_mocks.MockSMTP_SSL)
