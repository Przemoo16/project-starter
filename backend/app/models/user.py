from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, String
import sqlmodel


class User(sqlmodel.SQLModel, table=True):
    id: uuid.UUID | None = sqlmodel.Field(
        primary_key=True, index=True, default=uuid.uuid4
    )
    email: str = sqlmodel.Field(
        sa_column=Column(String, unique=True, index=True, nullable=False)
    )
    password: str
    confirmed_email: bool | None = False

    confirmation_email_key: uuid.UUID | None = sqlmodel.Field(default=uuid.uuid4)
    reset_password_key: uuid.UUID | None = sqlmodel.Field(default=uuid.uuid4)

    created_at: datetime | None = sqlmodel.Field(default=datetime.utcnow)
    updated_at: datetime | None = sqlmodel.Field(
        sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )
    last_login: datetime | None = None

    is_active: bool | None = True
    is_superuser: bool | None = False
