from fastapi import status

from app.exceptions.http import base


class InactiveUserError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "User is inactive"
        status_code = status.HTTP_403_FORBIDDEN
        super().__init__(status_code, detail, context)


class UserForbiddenError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "User is not allowed to access the resource"
        status_code = status.HTTP_403_FORBIDDEN
        super().__init__(status_code, detail, context)


class UserNotFoundError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "User not found"
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code, detail, context)


class UserAlreadyExistsError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "User already exists"
        status_code = status.HTTP_409_CONFLICT
        super().__init__(status_code, detail, context)


class InvalidPasswordError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "The password is invalid"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, detail, context)


class EmailAlreadyConfirmedError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Email has already been confirmed"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, detail, context)


class EmailConfirmationTokenExpiredError(base.HTTPException):
    def __init__(
        self, detail: base.Detail = None, context: base.Context = None
    ) -> None:
        detail = "Email confirmation token expired"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, detail, context)
