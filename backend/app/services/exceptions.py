import typing

import fastapi
from fastapi import status

Context = dict[str, typing.Any]


class ResourceExceptionCase(fastapi.HTTPException):
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


class UnauthorizedError(ResourceExceptionCase):
    def __init__(self, context: Context | None = None) -> None:
        status_code = status.HTTP_401_UNAUTHORIZED
        details = "Invalid credentials"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, details, context, headers)


class ForbiddenError(ResourceExceptionCase):
    def __init__(self, context: Context | None = None) -> None:
        status_code = status.HTTP_403_FORBIDDEN
        details = "Forbidden access"
        super().__init__(status_code, details, context)


class NotFoundError(ResourceExceptionCase):
    def __init__(self, context: Context | None = None) -> None:
        status_code = status.HTTP_404_NOT_FOUND
        details = "Resource not found"
        super().__init__(status_code, details, context)


class ConflictError(ResourceExceptionCase):
    def __init__(self, context: Context | None = None) -> None:
        status_code = status.HTTP_409_CONFLICT
        details = "Resource already exists"
        super().__init__(status_code, details, context)
