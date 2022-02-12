import typing

import fastapi

from app.models import exception

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
        self.context = context

    @property
    def doc(self) -> dict[int, dict[str, typing.Any]]:
        return {
            self.status_code: {
                "model": exception.ExceptionContent,
                "description": self.detail,
                "headers": self.headers,
            }
        }
