import typing

from fastapi import testclient
import pytest
import pytest_asyncio
from sqlalchemy import orm
from sqlalchemy.ext import asyncio
import sqlmodel
from sqlmodel import pool

from app import (  # noqa: F401 # pylint: disable=unused-import # Detect all models
    main,
    models,
)
from app.db import base

TEST_DB_ENGINE = "sqlite+aiosqlite://"

AsyncSession = asyncio.AsyncSession


@pytest.fixture(name="engine", scope="session")
def engine_fixture() -> typing.Generator[asyncio.AsyncEngine, None, None]:
    yield asyncio.create_async_engine(
        TEST_DB_ENGINE,
        connect_args={"check_same_thread": False},
        poolclass=pool.StaticPool,
    )


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
    engine: asyncio.AsyncEngine, create_tables: None  # pylint: disable=unused-argument
) -> typing.AsyncGenerator[AsyncSession, None]:
    async_session = orm.sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(
    session: AsyncSession,
) -> typing.Generator[testclient.TestClient, None, None]:
    main.app.dependency_overrides[base.get_session] = lambda: session
    client = testclient.TestClient(main.app)
    yield client
    main.app.dependency_overrides.clear()
