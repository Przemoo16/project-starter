import datetime
import typing
import uuid

import pydantic
import sqlmodel

from app.config import general
from app.models import base, helpers

if typing.TYPE_CHECKING:
    # For relationships, models with lazy annotations has to be used directly and
    # not via module (reset_password.ResetPasswordToken)
    from app.models.reset_password import ResetPasswordToken, ResetPasswordTokenID

UserID: typing.TypeAlias = uuid.UUID
UserEmail: typing.TypeAlias = pydantic.EmailStr
UserPassword: typing.TypeAlias = str
UserName: typing.TypeAlias = str
UserConfirmedEmail: typing.TypeAlias = bool
UserConfirmationEmailKey: typing.TypeAlias = uuid.UUID
UserCreatedAt: typing.TypeAlias = datetime.datetime
UserUpdatedAt: typing.TypeAlias = datetime.datetime
UserLastLogin: typing.TypeAlias = datetime.datetime
UserIsActive: typing.TypeAlias = bool

settings = general.get_settings()

USER_NAME_MIN_LENGTH = 4
USER_NAME_MAX_LENGTH = 64


class UserBase(base.BaseModel):
    email: UserEmail = sqlmodel.Field(index=True, sa_column_kwargs={"unique": True})
    password: UserPassword  # In database it's a hash so it doesn't have a strict length
    name: UserName = sqlmodel.Field(
        min_length=USER_NAME_MIN_LENGTH, max_length=USER_NAME_MAX_LENGTH
    )


class User(UserBase, table=True):
    # For the primary key, nullable has to be explicitly set up to False, otherwise it
    # is set to True and alembic produces unnecessary entries in migrations.
    id: UserID = sqlmodel.Field(
        primary_key=True, default_factory=helpers.generate_fixed_uuid, nullable=False
    )
    confirmed_email: UserConfirmedEmail = False
    confirmation_email_key: UserConfirmationEmailKey = sqlmodel.Field(
        index=True,
        default_factory=helpers.generate_fixed_uuid,
        sa_column_kwargs={"unique": True},
    )
    created_at: UserCreatedAt = sqlmodel.Field(default_factory=helpers.get_utcnow)
    updated_at: UserUpdatedAt = sqlmodel.Field(
        default_factory=helpers.get_utcnow,
        sa_column_kwargs={"onupdate": helpers.get_utcnow},
    )
    last_login: UserLastLogin | None = None
    reset_password_tokens: list["ResetPasswordToken"] = sqlmodel.Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )

    @property
    def is_active(self) -> UserIsActive:
        return self.confirmed_email


class UserCreate(UserBase):
    password: UserPassword = sqlmodel.Field(
        min_length=settings.USER_PASSWORD_MIN_LENGTH,
        max_length=settings.USER_PASSWORD_MAX_LENGTH,
    )


class UserFilters(base.PydanticBaseModel):
    id: UserID | None = None
    email: UserEmail | None = None
    confirmation_email_key: UserConfirmationEmailKey | None = None


class UserUpdateAPI(base.PydanticBaseModel):
    name: UserName | None = sqlmodel.Field(
        default=None, min_length=USER_NAME_MIN_LENGTH, max_length=USER_NAME_MAX_LENGTH
    )


class UserUpdate(UserUpdateAPI):
    password: UserPassword | None = None
    confirmed_email: UserConfirmedEmail | None = None
    last_login: UserLastLogin | None = None


class UserRead(base.BaseModel):
    id: UserID
    email: UserEmail
    name: UserName


class UserChangePassword(base.BaseModel):
    current_password: UserPassword
    new_password: UserPassword = sqlmodel.Field(
        min_length=settings.USER_PASSWORD_MIN_LENGTH,
        max_length=settings.USER_PASSWORD_MAX_LENGTH,
    )


class UserSetPassword(base.BaseModel):
    token: "ResetPasswordTokenID"
    password: UserPassword = sqlmodel.Field(
        min_length=settings.USER_PASSWORD_MIN_LENGTH,
        max_length=settings.USER_PASSWORD_MAX_LENGTH,
    )
