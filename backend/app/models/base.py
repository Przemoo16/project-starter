import orjson
import pydantic
import sqlmodel
from sqlmodel.sql import expression

from app.models import helpers
from app.utils import converters

# Bypassing a warning about caching
# TODO: Remove when https://github.com/tiangolo/sqlmodel/issues/189 is resolved
expression.SelectOfScalar.inherit_cache = True  # type: ignore
expression.Select.inherit_cache = True  # type: ignore


class BaseModel(sqlmodel.SQLModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = helpers.orjson_dumps
        alias_generator = converters.to_camel
        allow_population_by_field_name = True


class PydanticBaseModel(pydantic.BaseModel):
    """
    Pydantic model to update user.

    Currently exclude_unset is not working with sqlmodel.SQLModel
    #TODO: Delete and change all child to inherit from base.BaseModel when
    https://github.com/tiangolo/sqlmodel/issues/87 is resolved.
    """

    class Config:
        json_loads = orjson.loads
        json_dumps = helpers.orjson_dumps
        alias_generator = converters.to_camel
        allow_population_by_field_name = True
