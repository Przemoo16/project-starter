import typing

import fastapi

Context = dict[str, typing.Any]


class AppException(Exception):
    pass


class ResourceException(fastapi.HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        context: Context | None = None,
        headers: dict[str, typing.Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
        self.exception_case = self.__class__.__name__
        self.context = context
