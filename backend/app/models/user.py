from datetime import datetime
import uuid

import sqlmodel

from app.models import helpers


class User(sqlmodel.SQLModel, table=True):
    id: uuid.UUID | None = sqlmodel.Field(
        primary_key=True, index=True, default_factory=helpers.generate_fixed_uuid
    )
    email: str = sqlmodel.Field(index=True, sa_column_kwargs={"unique": True})
    password: str
    confirmed_email: bool | None = False

    confirmation_email_key: uuid.UUID | None = sqlmodel.Field(
        default_factory=helpers.generate_fixed_uuid
    )
    reset_password_key: uuid.UUID | None = sqlmodel.Field(
        default_factory=helpers.generate_fixed_uuid
    )

    created_at: datetime | None = sqlmodel.Field(default_factory=helpers.get_utcnow)
    updated_at: datetime | None = sqlmodel.Field(
        default_factory=helpers.get_utcnow,
        sa_column_kwargs={"onupdate": helpers.get_utcnow},
    )
    last_login: datetime | None = None

    is_active: bool | None = True
    is_superuser: bool | None = False
