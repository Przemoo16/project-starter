import orjson
import sqlmodel
from sqlmodel.sql import expression

from app.models import helpers

# Bypassing a warning about caching
# TODO: Remove when https://github.com/tiangolo/sqlmodel/issues/189 is resolved
expression.SelectOfScalar.inherit_cache = True  # type: ignore
expression.Select.inherit_cache = True  # type: ignore


class BaseModel(sqlmodel.SQLModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = helpers.orjson_dumps
        alias_generator = helpers.to_camel
        allow_population_by_field_name = True
