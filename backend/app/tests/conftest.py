from typing import AsyncGenerator, Generator

from fastapi import testclient
import pytest
import pytest_asyncio
from sqlalchemy import orm
from sqlalchemy.ext import asyncio
import sqlmodel
from sqlmodel import pool

from app import database, main
from app import models  # noqa: F401 # pylint: disable=unused-import # Detect all models

TEST_DB_ENGINE = "sqlite+aiosqlite://"


@pytest.fixture(name="engine", scope="session")
def engine_fixture() -> Generator[asyncio.AsyncEngine, None, None]:
    yield asyncio.create_async_engine(
        TEST_DB_ENGINE,
        connect_args={"check_same_thread": False},
        poolclass=pool.StaticPool,
    )


@pytest_asyncio.fixture(name="create_tables")
async def create_tables_fixture(
    engine: asyncio.AsyncEngine,
) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(sqlmodel.SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(name="session")
async def session_fixture(
    engine: asyncio.AsyncEngine, create_tables: None  # pylint: disable=unused-argument
) -> AsyncGenerator[asyncio.AsyncSession, None]:
    async_session = orm.sessionmaker(
        engine, class_=asyncio.AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(
    session: asyncio.AsyncSession,
) -> Generator[testclient.TestClient, None, None]:
    main.app.dependency_overrides[database.get_session] = lambda: session
    client = testclient.TestClient(main.app)
    yield client
    main.app.dependency_overrides.clear()
