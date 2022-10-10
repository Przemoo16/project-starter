import typing

import pydantic

from app.models import base

TotalResults: typing.TypeAlias = int

PaginationOffset: typing.TypeAlias = pydantic.conint(ge=0)  # type: ignore


class Pagination(base.BaseModel):
    offset: PaginationOffset = 0
    limit: pydantic.PositiveInt | None = None


class PaginationResponse(base.BaseModel):
    total: TotalResults
