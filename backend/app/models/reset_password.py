import datetime
import typing
import uuid

import sqlmodel

from app.config import general
from app.models import base, helpers
from app.models import user as user_models

settings = general.get_settings()

ResetPasswordTokenID: typing.TypeAlias = uuid.UUID
ResetPasswordTokenExpireAt: typing.TypeAlias = datetime.datetime


def get_expiration_time() -> datetime.datetime:
    return helpers.get_utcnow() + settings.RESET_PASSWORD_TOKEN_EXPIRES


class ResetPasswordTokenBase(base.BaseModel):
    user_id: user_models.UserID = sqlmodel.Field(foreign_key="user.id", index=True)


class ResetPasswordToken(ResetPasswordTokenBase, table=True):
    id: ResetPasswordTokenID = sqlmodel.Field(
        primary_key=True, default_factory=helpers.get_uuid4
    )
    expire_at: ResetPasswordTokenExpireAt = sqlmodel.Field(
        default_factory=get_expiration_time
    )
    created_at: datetime.datetime = sqlmodel.Field(default_factory=helpers.get_utcnow)
    updated_at: datetime.datetime = sqlmodel.Field(
        default_factory=helpers.get_utcnow,
        sa_column_kwargs={"onupdate": helpers.get_utcnow},
    )
    user: user_models.User = sqlmodel.Relationship(
        back_populates="reset_password_tokens",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def is_expired(self) -> bool:
        return helpers.get_utcnow() > self.expire_at


class ResetPasswordTokenCreate(ResetPasswordTokenBase):
    pass


class ResetPasswordTokenFilters(base.BaseModel):
    id: ResetPasswordTokenID | None = None
    user_id: user_models.UserID | None = None


class ResetPasswordTokenUpdate(base.BaseModel):
    expire_at: ResetPasswordTokenExpireAt | None = None
