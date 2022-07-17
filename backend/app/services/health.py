import socket
import typing

from kombu import exceptions as kombu_exceptions
import redis
from redis import exceptions as redis_exceptions
from sqlalchemy import exc
import sqlmodel

from app.config import general
from app.exceptions.http import health as health_exceptions
from app.models import user as user_models
from app.tasks import health as health_tasks

if typing.TYPE_CHECKING:
    from app.config import db

settings = general.get_settings()


class HealthService:
    OK_FLAG = "OK"

    def __init__(self, session: "db.AsyncSession"):
        self.session = session

    async def check_health(self) -> None:
        healths = {
            "database": await self._check_database(),
            "redis": self._check_redis(),
            "celery": self._check_celery(),
        }
        if any(health != self.OK_FLAG for health in healths.values()):
            raise health_exceptions.HealthError(context=healths)

    async def _check_database(self) -> str:
        try:
            await self._execute_test_clause()
        except (exc.InterfaceError, socket.gaierror) as e:
            return str(e)
        return self.OK_FLAG

    async def _execute_test_clause(self) -> None:
        (await self.session.execute(sqlmodel.select(user_models.User).limit(1))).all()

    def _check_redis(self) -> str:
        try:
            redis.Redis.from_url(settings.REDIS_URL).ping()
        except redis_exceptions.ConnectionError as e:
            return str(e)
        return self.OK_FLAG

    def _check_celery(self) -> str:
        try:
            health_tasks.check_health.delay()
        except kombu_exceptions.OperationalError as e:
            return str(e)
        return self.OK_FLAG
