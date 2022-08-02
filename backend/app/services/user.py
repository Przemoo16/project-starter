import datetime
import logging
import typing

from sqlalchemy import exc

from app.config import general
from app.exceptions.http import user as user_exceptions
from app.models import pagination as pagination_models
from app.models import reset_password as reset_password_models
from app.models import user as user_models
from app.services import base
from app.services import reset_password as reset_password_services
from app.tasks import user as user_tasks
from app.utils import auth

if typing.TYPE_CHECKING:
    from app.config import db

log = logging.getLogger(__name__)

settings = general.get_settings()


class UserService:
    def __init__(self, session: "db.AsyncSession"):
        self.crud = UserCRUD(session)
        self.reset_password_service = reset_password_services.ResetPasswordService(
            session
        )

    async def create_user(self, user: user_models.UserCreate) -> user_models.User:
        user.password = auth.hash_password(user.password)
        try:
            user_db = await self.crud.create(user)
        except exc.IntegrityError as e:
            raise user_exceptions.UserAlreadyExistsError(
                context={"email": user.email}
            ) from e
        user_tasks.send_email_to_confirm_email.delay(
            user_db.email, user_db.email_confirmation_token
        )
        log.info("The task to send email to confirm email has been invoked")
        return user_db

    async def get_users(
        self,
        filters: user_models.UserFilters,
        pagination: pagination_models.Pagination = pagination_models.Pagination(),
    ) -> list[user_models.User]:
        return await self.crud.read_many(filters, pagination)

    async def get_user(self, filters: user_models.UserFilters) -> user_models.User:
        try:
            return await self.crud.read_one(filters)
        except exc.NoResultFound as e:
            filters_data = filters.dict(exclude_unset=True)
            raise user_exceptions.UserNotFoundError(context=filters_data) from e

    async def get_active_user(
        self, filters: user_models.UserFilters
    ) -> user_models.User:
        user = await self.get_user(filters)
        if not user.is_active:
            raise user_exceptions.InactiveUserError(context={"id": user.id})
        return user

    async def update_user(
        self, user_db: user_models.User, user_update: user_models.UserUpdate
    ) -> user_models.User:
        if user_update.password:
            user_update.password = auth.hash_password(user_update.password)
        return await self.crud.update(user_db, user_update)

    async def delete_user(self, user: user_models.User) -> None:
        await self.crud.delete(user)

    async def count_users(
        self, filters: user_models.UserFilters
    ) -> pagination_models.TotalResults:
        return await self.crud.count(filters)

    async def change_password(
        self,
        user: user_models.User,
        current_password: user_models.UserPassword,
        new_password: user_models.UserPassword,
    ) -> None:
        if not auth.verify_password(current_password, user.password):
            raise user_exceptions.InvalidPasswordError()
        user_update = user_models.UserUpdate(password=auth.hash_password(new_password))
        await self.crud.update(user, user_update)

    async def confirm_email(self, user: user_models.User) -> None:
        context = {"id": user.email_confirmation_token}
        if user.confirmed_email:
            raise user_exceptions.EmailAlreadyConfirmedError(context=context)
        if _token_expired(user):
            raise user_exceptions.EmailConfirmationTokenExpiredError(context=context)
        user_update = user_models.UserUpdate(confirmed_email=True)
        await self.crud.update(user, user_update)

    async def reset_password(self, user: user_models.User) -> None:
        token = await self.reset_password_service.create_token(
            reset_password_models.ResetPasswordTokenCreate(user_id=user.id)
        )
        user_tasks.send_email_to_reset_password.delay(user.email, token.id)
        log.info("The task to send email to reset password has been invoked")

    async def set_password(
        self,
        token: reset_password_models.ResetPasswordTokenID,
        password: user_models.UserPassword,
    ) -> None:
        token_filters = reset_password_models.ResetPasswordTokenFilters(id=token)
        token_db = await self.reset_password_service.get_valid_token(token_filters)
        user = token_db.user
        if not user.is_active:
            raise user_exceptions.InactiveUserError(context={"id": user.id})
        user_update = user_models.UserUpdate(password=auth.hash_password(password))
        await self.crud.update(user, user_update)
        await self.reset_password_service.force_to_expire(token_db)


def _token_expired(user: user_models.User) -> bool:
    expiration_date = user.created_at + settings.EMAIL_CONFIRMATION_TOKEN_EXPIRES
    return expiration_date < datetime.datetime.utcnow()


class UserCRUD(base.AppCRUD):
    model = user_models.User
