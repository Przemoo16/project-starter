from fastapi import status

from app.exceptions.http import base


class InvalidCredentials(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Invalid credentials"
        status_code = status.HTTP_401_UNAUTHORIZED
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, context, headers)


class RevokedTokenError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Token is revoked"
        status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code, detail, context)


class InactiveUserError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "User is inactive"
        status_code = status.HTTP_403_FORBIDDEN
        super().__init__(status_code, detail, context)


class InvalidTokenError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Invalid token"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, detail, context)


class RefreshTokenRequiredError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Refresh token required"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, detail, context)
