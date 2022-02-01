from typing import Any, Callable

import orjson
import sqlmodel
from sqlmodel.sql import expression

# Bypassing a warning about caching
# TODO: Remove when https://github.com/tiangolo/sqlmodel/issues/189 is resolved
expression.SelectOfScalar.inherit_cache = True  # type: ignore
expression.Select.inherit_cache = True  # type: ignore


def orjson_dumps(data: Any, *, default: Callable[[Any], Any] | None) -> str:
    return orjson.dumps(
        data, default=default, option=orjson.OPT_NAIVE_UTC | orjson.OPT_UTC_Z
    ).decode()


class BaseModel(sqlmodel.SQLModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
