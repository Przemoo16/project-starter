import orjson
import sqlmodel

from app.models import helpers
from app.utils import converters


class BaseModel(sqlmodel.SQLModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = helpers.orjson_dumps
        alias_generator = converters.to_camel
        allow_population_by_field_name = True
