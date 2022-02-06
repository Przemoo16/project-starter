import datetime
import logging
import typing

from sqlalchemy import exc
import sqlmodel

from app.config import general
from app.models import user as user_models
from app.services import auth, base, exceptions

log = logging.getLogger(__name__)

settings = general.get_settings()


class UserService(base.AppService):
    async def create_user(self, user: user_models.UserCreate) -> user_models.User:
        user.password = auth.hash_password(user.password)
        try:
            return await UserCRUD(self.session).create(user)
        except exc.IntegrityError as e:
            raise exceptions.ConflictError({"email": user.email}) from e

    async def get_user(self, user_id: user_models.UserID) -> user_models.User:
        try:
            return await UserCRUD(self.session).read(id=user_id)
        except exc.NoResultFound as e:
            raise exceptions.NotFoundError({"id": user_id}) from e

    async def update_user(
        self, user_id: user_models.UserID, user: user_models.UserUpdate
    ) -> user_models.User:
        user_crud_service = UserCRUD(self.session)
        if user.password:
            user.password = auth.hash_password(user.password)
        try:
            user_db = await user_crud_service.read(id=user_id)
        except exc.NoResultFound as e:
            raise exceptions.NotFoundError({"id": user_id}) from e
        user_data = user.dict(exclude_unset=True)
        return await user_crud_service.update(user_db, **user_data)

    async def delete_user(self, user_id: user_models.UserID) -> None:
        user_crud_service = UserCRUD(self.session)
        try:
            user_db = await user_crud_service.read(id=user_id)
        except exc.NoResultFound as e:
            raise exceptions.NotFoundError({"id": user_id}) from e
        return await user_crud_service.delete(user_db)

    async def confirm_email(self, key: user_models.ConfirmationEmailKey) -> bool:
        not_found_exception = exceptions.NotFoundError({"key": key})
        try:
            user_db = await UserCRUD(self.session).read(confirmation_email_key=key)
        except exc.NoResultFound as e:
            raise not_found_exception from e
        if not await self._confirm_email(user_db):
            raise not_found_exception
        return True

    async def _confirm_email(self, user: user_models.User) -> bool:
        if user.confirmed_email:
            log.info("Email already confirmed")
            return False
        expiration_date = user.created_at + datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS
        )
        if expiration_date < datetime.datetime.utcnow():
            log.info("Email has not been confirmed because confirmation email expired")
            return False
        await UserCRUD(self.session).update(user, confirmed_email=True)
        log.info("Email has been confirmed")
        return True


class UserCRUD(base.AppCRUD):
    async def create(self, user: user_models.UserCreate) -> user_models.User:
        db_user = user_models.User.from_orm(user)
        return await self.save(db_user)

    async def read(self, **kwargs: typing.Any) -> user_models.User:
        read_statement = sqlmodel.select(user_models.User)
        for attr, value in kwargs.items():
            read_statement = read_statement.where(
                getattr(user_models.User, attr) == value
            )
        result = await self.session.execute(read_statement)
        return result.scalar_one()

    async def update(
        self, user: user_models.User, **kwargs: typing.Any
    ) -> user_models.User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        return await self.save(user)

    async def delete(self, user: user_models.User) -> None:
        await self.session.delete(user)
        await self.session.commit()
