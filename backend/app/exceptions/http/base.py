import typing

import fastapi

from app.models import exception

Detail: typing.TypeAlias = str | None
Context: typing.TypeAlias = dict[str, typing.Any] | None


# Multiple inheritance to surpass the pylint bad-exception-context error
class HTTPException(fastapi.HTTPException, Exception):
    def __init__(
        self,
        status_code: int,
        detail: Detail = None,
        context: Context = None,
        headers: dict[str, typing.Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
        self.case = self.__class__.__name__
        self.context = context

    @property
    def doc(self) -> dict[int | str, dict[str, typing.Any]]:
        return {
            self.status_code: {
                "model": exception.ExceptionContent,
                "description": self.detail,
                "headers": self.headers,
                "content": {
                    "application/json": {
                        "example": {
                            "case": self.case,
                            "detail": self.detail,
                            "context": self.context or {},
                        },
                    }
                },
            }
        }
