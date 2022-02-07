from fastapi import status

from app.exceptions import base


class BadRequestError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_400_BAD_REQUEST
        details = "Bad request"
        super().__init__(status_code, details, context)


class UnauthorizedError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_401_UNAUTHORIZED
        details = "Invalid credentials"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, details, context, headers)


class ForbiddenError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_403_FORBIDDEN
        details = "Forbidden access"
        super().__init__(status_code, details, context)


class NotFoundError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_404_NOT_FOUND
        details = "Resource not found"
        super().__init__(status_code, details, context)


class ConflictError(base.ResourceException):
    def __init__(self, context: base.Context | None = None) -> None:
        status_code = status.HTTP_409_CONFLICT
        details = "Resource already exists"
        super().__init__(status_code, details, context)
