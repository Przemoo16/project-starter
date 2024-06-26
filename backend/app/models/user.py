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
UserEmailConfirmationToken: typing.TypeAlias = uuid.UUID
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
    id: UserID = sqlmodel.Field(primary_key=True, default_factory=helpers.get_uuid4)
    confirmed_email: UserConfirmedEmail = False
    email_confirmation_token: UserEmailConfirmationToken = sqlmodel.Field(
        index=True,
        default_factory=helpers.get_uuid4,
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


class UserFilters(base.BaseModel):
    id: UserID | None = None
    email: UserEmail | None = None
    email_confirmation_token: UserEmailConfirmationToken | None = None


class UserUpdateAPI(base.BaseModel):
    # FIXME: It is possible to pass `null` as the `name` field and thus break app.
    # Use exclude_none when performing update or annotate the field as string and use
    # a default value if no better solution will be found
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
