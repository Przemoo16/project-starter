import enum
import typing

from app.models import base


class SortingWay(enum.Enum):
    ASC = enum.auto()
    DESC = enum.auto()


class Sorting(base.BaseModel):
    column: typing.Any
    way: SortingWay
