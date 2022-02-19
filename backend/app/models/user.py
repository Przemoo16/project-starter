from datetime import datetime
import typing
import uuid

import pydantic
import sqlmodel

from app.models import base, helpers

UserID: typing.TypeAlias = uuid.UUID
UserEmail: typing.TypeAlias = pydantic.EmailStr
UserPassword: typing.TypeAlias = str
UserConfirmedEmail: typing.TypeAlias = bool
UserConfirmationEmailKey: typing.TypeAlias = uuid.UUID
UserResetPasswordKey: typing.TypeAlias = uuid.UUID
UserLastLogin: typing.TypeAlias = datetime


class User(base.BaseModel, table=True):
    id: UserID = sqlmodel.Field(
        primary_key=True, index=True, default_factory=helpers.generate_fixed_uuid
    )
    email: UserEmail = sqlmodel.Field(index=True, sa_column_kwargs={"unique": True})
    password: UserPassword
    confirmed_email: UserConfirmedEmail = False
    confirmation_email_key: UserConfirmationEmailKey = sqlmodel.Field(
        default_factory=helpers.generate_fixed_uuid
    )
    reset_password_key: UserResetPasswordKey = sqlmodel.Field(
        default_factory=helpers.generate_fixed_uuid
    )
    created_at: datetime = sqlmodel.Field(default_factory=helpers.get_utcnow)
    updated_at: datetime = sqlmodel.Field(
        default_factory=helpers.get_utcnow,
        sa_column_kwargs={"onupdate": helpers.get_utcnow},
    )
    last_login: UserLastLogin | None = None

    @property
    def is_active(self) -> bool:
        return self.confirmed_email


class UserCreate(base.BaseModel):
    email: UserEmail
    password: UserPassword


class UserRead(base.PydanticBaseModel):
    id: UserID | None = None
    email: UserEmail | None = None
    confirmation_email_key: UserConfirmationEmailKey | None = None
    reset_password_key: UserResetPasswordKey | None = None


class UserUpdateAPI(base.PydanticBaseModel):
    email: UserEmail | None = None
    password: UserPassword | None = None


class UserUpdate(UserUpdateAPI):
    confirmed_email: UserConfirmedEmail | None = None
    last_login: UserLastLogin | None = None
    reset_password_key: UserResetPasswordKey | None = None


class UserOutput(base.BaseModel):
    id: UserID
    email: UserEmail
