import socket
import typing
from unittest import mock

import pytest
from kombu import exceptions as kombu_exceptions
from redis import exceptions as redis_exceptions
from sqlalchemy import exc

from app.exceptions.http import health as health_exceptions
from app.services import health as health_services

if typing.TYPE_CHECKING:
    from app.tests import conftest


@pytest.mark.anyio
async def test_health_service_check_health(session: "conftest.AsyncSession") -> None:
    await health_services.HealthService(session).check_health()


@pytest.mark.anyio
@mock.patch("app.services.health.HealthService._execute_test_clause")
@mock.patch("redis.Redis.ping")
@mock.patch("app.services.health.health_tasks.check_health.delay")
@pytest.mark.parametrize(
    "error",
    [
        exc.InterfaceError(
            statement="Test statement", params="Test params", orig=Exception
        ),
        socket.gaierror("gaierror"),
    ],
)
async def test_health_service_check_health_database_error(
    mock_check_health_task: mock.MagicMock,  # pylint: disable=unused-argument
    mock_redis: mock.MagicMock,  # pylint: disable=unused-argument
    mock_execute_test_clause: mock.AsyncMock,
    error: Exception,
    session: "conftest.AsyncSession",
) -> None:
    mock_execute_test_clause.side_effect = error

    with pytest.raises(health_exceptions.HealthError) as exc_info:
        await health_services.HealthService(session).check_health()
    assert exc_info.value.context == {
        "database": str(error),
        "redis": health_services.HealthService.OK_FLAG,
        "celery": health_services.HealthService.OK_FLAG,
    }


@pytest.mark.anyio
@mock.patch("app.services.health.HealthService._execute_test_clause")
@mock.patch("redis.Redis.ping")
@mock.patch("app.services.health.health_tasks.check_health.delay")
async def test_health_service_check_health_redis_error(
    mock_check_health_task: mock.MagicMock,  # pylint: disable=unused-argument
    mock_redis: mock.MagicMock,
    mock_execute_test_clause: mock.AsyncMock,  # pylint: disable=unused-argument
    session: "conftest.AsyncSession",
) -> None:
    error_message = "Redis error"
    mock_redis.side_effect = redis_exceptions.ConnectionError(error_message)

    with pytest.raises(health_exceptions.HealthError) as exc_info:
        await health_services.HealthService(session).check_health()
    assert exc_info.value.context == {
        "database": health_services.HealthService.OK_FLAG,
        "redis": error_message,
        "celery": health_services.HealthService.OK_FLAG,
    }


@pytest.mark.anyio
@mock.patch("app.services.health.HealthService._execute_test_clause")
@mock.patch("redis.Redis.ping")
@mock.patch("app.services.health.health_tasks.check_health.delay")
async def test_health_service_check_health_celery_error(
    mock_check_health_task: mock.MagicMock,
    mock_redis: mock.MagicMock,  # pylint: disable=unused-argument
    mock_execute_test_clause: mock.AsyncMock,  # pylint: disable=unused-argument
    session: "conftest.AsyncSession",
) -> None:
    error_message = "Celery error"
    mock_check_health_task.side_effect = kombu_exceptions.OperationalError(
        error_message
    )

    with pytest.raises(health_exceptions.HealthError) as exc_info:
        await health_services.HealthService(session).check_health()
    assert exc_info.value.context == {
        "database": health_services.HealthService.OK_FLAG,
        "redis": health_services.HealthService.OK_FLAG,
        "celery": error_message,
    }
