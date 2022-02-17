import typing

from app.models import base

ExceptionContext: typing.TypeAlias = dict[str, typing.Any] | list[typing.Any] | None


class ExceptionContent(base.BaseModel):
    case: str
    detail: str
    context: ExceptionContext
