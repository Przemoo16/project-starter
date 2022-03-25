import typing

import pydantic

from app.models import base

TotalResults: typing.TypeAlias = int

PaginationOffset: typing.TypeAlias = pydantic.conint(ge=0)  # type: ignore
PaginationLimit: typing.TypeAlias = pydantic.PositiveInt | None


class Pagination(base.BaseModel):
    offset: PaginationOffset = 0
    limit: PaginationLimit = None


class PaginationResponse(base.BaseModel):
    total: TotalResults
