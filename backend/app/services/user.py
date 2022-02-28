import datetime
import logging

from sqlalchemy import exc

from app.config import general
from app.exceptions.http import user as user_exceptions
from app.models import helpers
from app.models import pagination as pagination_models
from app.models import user as user_models
from app.services import auth, base
from app.tasks import user as user_tasks

log = logging.getLogger(__name__)

settings = general.get_settings()


class UserService(base.AppService):
    async def create_user(self, user: user_models.UserCreate) -> user_models.User:
        user.password = auth.hash_password(user.password)
        try:
            user_db = await UserCRUD(self.session).create(user)
        except exc.IntegrityError as e:
            raise user_exceptions.UserAlreadyExistsError(
                context={"email": user.email}
            ) from e
        user_tasks.send_email_to_confirm_email.delay(
            user_db.email, user_db.confirmation_email_key
        )
        log.info("The task to send email to confirm email has been invoked")
        return user_db

    async def get_users(
        self,
        filters: user_models.UserFilters,
        pagination: pagination_models.Pagination = pagination_models.Pagination(),
    ) -> list[user_models.User]:
        return await UserCRUD(self.session).read_many(filters, pagination)

    async def get_user(self, filters: user_models.UserFilters) -> user_models.User:
        try:
            return await UserCRUD(self.session).read_one(filters)
        except exc.NoResultFound as e:
            filters_data = filters.dict(exclude_unset=True)
            raise user_exceptions.UserNotFoundError(context=filters_data) from e

    async def update_user(
        self, user_id: user_models.UserID, user: user_models.UserUpdate
    ) -> user_models.User:
        user_crud_service = UserCRUD(self.session)
        if user.password:
            user.password = auth.hash_password(user.password)
        user_filters = user_models.UserFilters(id=user_id)
        try:
            user_db = await user_crud_service.read_one(user_filters)
        except exc.NoResultFound as e:
            raise user_exceptions.UserNotFoundError(context={"id": user_id}) from e
        return await user_crud_service.update(user_db, user)

    async def delete_user(self, user_id: user_models.UserID) -> None:
        user_crud_service = UserCRUD(self.session)
        user_filters = user_models.UserFilters(id=user_id)
        try:
            user_db = await user_crud_service.read_one(user_filters)
        except exc.NoResultFound as e:
            raise user_exceptions.UserNotFoundError(context={"id": user_id}) from e
        await user_crud_service.delete(user_db)

    async def count_users(
        self, filters: user_models.UserFilters
    ) -> pagination_models.TotalResults:
        return await UserCRUD(self.session).count(filters)

    async def confirm_email(self, key: user_models.UserConfirmationEmailKey) -> None:
        not_found_exception = user_exceptions.UserNotFoundError(context={"key": key})
        user_filters = user_models.UserFilters(confirmation_email_key=key)
        try:
            user_db = await UserCRUD(self.session).read_one(user_filters)
        except exc.NoResultFound as e:
            raise not_found_exception from e
        if not can_confirm_email(user_db):
            raise not_found_exception
        user_update = user_models.UserUpdate(confirmed_email=True)
        await UserCRUD(self.session).update(user_db, user_update)

    async def request_reset_password(self, email: user_models.UserEmail) -> None:
        user_filters = user_models.UserFilters(email=email)
        try:
            user_db = await UserCRUD(self.session).read_one(user_filters)
        except exc.NoResultFound:
            log.info("Message has not been sent because user not found")
            return
        user_tasks.send_email_to_reset_password.delay(
            user_db.email, user_db.reset_password_key
        )
        log.info("The task to send email to reset password has been invoked")

    async def reset_password(
        self,
        key: user_models.UserResetPasswordKey,
        password: user_models.UserPassword,
    ) -> None:
        user_filters = user_models.UserFilters(reset_password_key=key)
        try:
            user_db = await UserCRUD(self.session).read_one(user_filters)
        except exc.NoResultFound as e:
            raise user_exceptions.UserNotFoundError(context={"key": key}) from e
        user_update = user_models.UserUpdate(
            password=auth.hash_password(password),
            reset_password_key=helpers.generate_fixed_uuid(),
        )
        await UserCRUD(self.session).update(user_db, user_update)


def can_confirm_email(user: user_models.User) -> bool:
    if user.confirmed_email:
        log.info("Email already confirmed")
        return False
    expiration_date = user.created_at + datetime.timedelta(
        days=settings.ACCOUNT_ACTIVATION_DAYS
    )
    if expiration_date < datetime.datetime.utcnow():
        log.info("Confirmation email expired")
        return False
    return True


class UserCRUD(base.AppCRUD):
    async def create(self, user: user_models.UserCreate) -> user_models.User:
        return await self._create(user_models.User, user)

    async def read_many(
        self,
        filters: user_models.UserFilters,
        pagination: pagination_models.Pagination = pagination_models.Pagination(),
    ) -> list[user_models.User]:
        return await self._read_many(user_models.User, filters, pagination)

    async def read_one(self, filters: user_models.UserFilters) -> user_models.User:
        return await self._read_one(user_models.User, filters)

    async def update(
        self, user_db: user_models.User, user_update: user_models.UserUpdate
    ) -> user_models.User:
        return await self._update(user_db, user_update)

    async def delete(self, user: user_models.User) -> None:
        await self._delete(user)

    async def count(
        self, filters: user_models.UserFilters
    ) -> pagination_models.TotalResults:
        return await self._count(user_models.User, filters)
