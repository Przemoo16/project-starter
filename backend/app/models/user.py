from datetime import datetime
import typing
import uuid

import pydantic
import sqlmodel

from app.models import base, helpers

UserID: typing.TypeAlias = uuid.UUID
UserEmail: typing.TypeAlias = pydantic.EmailStr
UserPassword: typing.TypeAlias = str
UserConfirmationEmailKey: typing.TypeAlias = uuid.UUID
UserResetPasswordKey: typing.TypeAlias = uuid.UUID


class User(base.BaseModel, table=True):
    id: UserID = sqlmodel.Field(
        primary_key=True, index=True, default_factory=helpers.generate_fixed_uuid
    )
    email: UserEmail = sqlmodel.Field(index=True, sa_column_kwargs={"unique": True})
    password: UserPassword
    confirmed_email: bool = False
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
    last_login: datetime | None = None

    @property
    def is_active(self) -> bool:
        return self.confirmed_email


class UserCreate(base.BaseModel):
    email: UserEmail
    password: UserPassword


class UserRead(base.BaseModel):
    id: UserID
    email: UserEmail


class UserUpdate(pydantic.BaseModel):
    """
    Pydantic model to update user.

    Currently exclude_unset is not working with sqlmodel.SQLModel
    #TODO: Change to base.BaseModel when
    https://github.com/tiangolo/sqlmodel/issues/87 is resolved.
    """

    email: UserEmail | None = None
    password: UserPassword | None = None

    class Config:
        alias_generator = helpers.to_camel
        allow_population_by_field_name = True
