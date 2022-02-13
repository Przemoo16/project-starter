import typing

import orjson
import sqlmodel
from sqlmodel.sql import expression

from app.models import helpers

# Bypassing a warning about caching
# TODO: Remove when https://github.com/tiangolo/sqlmodel/issues/189 is resolved
expression.SelectOfScalar.inherit_cache = True  # type: ignore
expression.Select.inherit_cache = True  # type: ignore


def orjson_dumps(
    data: typing.Any, *, default: typing.Callable[[typing.Any], typing.Any] | None
) -> str:
    return orjson.dumps(
        data, default=default, option=orjson.OPT_NAIVE_UTC | orjson.OPT_UTC_Z
    ).decode()


class BaseModel(sqlmodel.SQLModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        alias_generator = helpers.to_camel
        allow_population_by_field_name = True
