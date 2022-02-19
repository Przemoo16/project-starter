import datetime
import logging

from sqlalchemy import exc
import sqlmodel

from app.config import general
from app.exceptions.http import user as user_exceptions
from app.models import helpers
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

    async def get_user(self, user: user_models.UserRead) -> user_models.User:
        try:
            return await UserCRUD(self.session).read(user)
        except exc.NoResultFound as e:
            user_data = user.dict(exclude_unset=True)
            raise user_exceptions.UserNotFoundError(context=user_data) from e

    async def update_user(
        self, user_id: user_models.UserID, user: user_models.UserUpdate
    ) -> user_models.User:
        user_crud_service = UserCRUD(self.session)
        if user.password:
            user.password = auth.hash_password(user.password)
        user_read = user_models.UserRead(id=user_id)
        try:
            user_db = await user_crud_service.read(user_read)
        except exc.NoResultFound as e:
            raise user_exceptions.UserNotFoundError(context={"id": user_id}) from e
        return await user_crud_service.update(user_db, user)

    async def delete_user(self, user_id: user_models.UserID) -> None:
        user_crud_service = UserCRUD(self.session)
        user_read = user_models.UserRead(id=user_id)
        try:
            user_db = await user_crud_service.read(user_read)
        except exc.NoResultFound as e:
            raise user_exceptions.UserNotFoundError(context={"id": user_id}) from e
        return await user_crud_service.delete(user_db)

    async def confirm_email(self, key: user_models.UserConfirmationEmailKey) -> None:
        not_found_exception = user_exceptions.UserNotFoundError(context={"key": key})
        user_read = user_models.UserRead(confirmation_email_key=key)
        try:
            user_db = await UserCRUD(self.session).read(user_read)
        except exc.NoResultFound as e:
            raise not_found_exception from e
        if not can_confirm_email(user_db):
            raise not_found_exception
        user_update = user_models.UserUpdate(confirmed_email=True)
        await UserCRUD(self.session).update(user_db, user_update)
        log.info("Email has been confirmed")

    async def request_reset_password(self, email: user_models.UserEmail | str) -> None:
        user_read = user_models.UserRead(email=email)
        try:
            user_db = await UserCRUD(self.session).read(user_read)
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
        user_read = user_models.UserRead(reset_password_key=key)
        try:
            user_db = await UserCRUD(self.session).read(user_read)
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
        db_user = user_models.User.from_orm(user)
        return await self.save(db_user)

    async def read(self, user: user_models.UserRead) -> user_models.User:
        user_data = user.dict(exclude_unset=True)
        read_statement = sqlmodel.select(user_models.User)
        for attr, value in user_data.items():
            read_statement = read_statement.where(
                getattr(user_models.User, attr) == value
            )
        result = await self.session.execute(read_statement)
        return result.scalar_one()

    async def update(
        self, user: user_models.User, user_update: user_models.UserUpdate
    ) -> user_models.User:
        user_data = user_update.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        return await self.save(user)

    async def delete(self, user: user_models.User) -> None:
        await self.session.delete(user)
        await self.session.commit()
