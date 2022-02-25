import datetime
import typing
import uuid

import pydantic
import sqlmodel

from app.config import general
from app.models import base, helpers

UserID: typing.TypeAlias = uuid.UUID
UserEmail: typing.TypeAlias = pydantic.EmailStr
UserPassword: typing.TypeAlias = str
UserConfirmedEmail: typing.TypeAlias = bool
UserConfirmationEmailKey: typing.TypeAlias = uuid.UUID
UserResetPasswordKey: typing.TypeAlias = uuid.UUID
UserCreatedAt: typing.TypeAlias = datetime.datetime
UserUpdatedAt: typing.TypeAlias = datetime.datetime
UserLastLogin: typing.TypeAlias = datetime.datetime
UserIsActive: typing.TypeAlias = bool

settings = general.get_settings()


class UserBase(base.BaseModel):
    email: UserEmail = sqlmodel.Field(index=True, sa_column_kwargs={"unique": True})
    password: UserPassword  # In database it's a hash so it doesn't have a strict length


class User(UserBase, table=True):
    # For the primary key, nullable has to be explicitly set up to False, otherwise it
    # is set to True and alembic produces unnecessary entries in migrations.
    id: UserID = sqlmodel.Field(
        primary_key=True, default_factory=helpers.generate_fixed_uuid, nullable=False
    )
    confirmed_email: UserConfirmedEmail = False
    confirmation_email_key: UserConfirmationEmailKey = sqlmodel.Field(
        index=True, default_factory=helpers.generate_fixed_uuid
    )
    reset_password_key: UserResetPasswordKey = sqlmodel.Field(
        index=True, default_factory=helpers.generate_fixed_uuid
    )
    created_at: UserCreatedAt = sqlmodel.Field(default_factory=helpers.get_utcnow)
    updated_at: UserUpdatedAt = sqlmodel.Field(
        default_factory=helpers.get_utcnow,
        sa_column_kwargs={"onupdate": helpers.get_utcnow},
    )
    last_login: UserLastLogin | None = None

    @property
    def is_active(self) -> UserIsActive:
        return self.confirmed_email


class UserCreate(UserBase):
    password: UserPassword = sqlmodel.Field(
        min_length=settings.USER_PASSWORD_MIN_LENGTH,
        max_length=settings.USER_PASSWORD_MAX_LENGTH,
    )


class UserRead(base.PydanticBaseModel):
    id: UserID | None = None
    email: UserEmail | None = None
    confirmation_email_key: UserConfirmationEmailKey | None = None
    reset_password_key: UserResetPasswordKey | None = None


class UserUpdateAPI(base.PydanticBaseModel):
    email: UserEmail | None = None
    password: UserPassword | None = sqlmodel.Field(
        default=None,
        min_length=settings.USER_PASSWORD_MIN_LENGTH,
        max_length=settings.USER_PASSWORD_MAX_LENGTH,
    )


class UserUpdate(UserUpdateAPI):
    password: UserPassword | None = None
    confirmed_email: UserConfirmedEmail | None = None
    last_login: UserLastLogin | None = None
    reset_password_key: UserResetPasswordKey | None = None


class UserOutput(base.BaseModel):
    id: UserID
    email: UserEmail
    is_active: UserIsActive
