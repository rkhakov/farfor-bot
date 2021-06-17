from factory.alchemy import SQLAlchemyModelFactory

from farfor_bot import models
from farfor_bot.database.core import SessionLocal
from farfor_bot.security import get_password_hash


USER_LOGIN = "user"
USER_PASSWORD = "user"


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    is_superuser = False
    is_admin = False
    login = USER_LOGIN
    hashed_password = get_password_hash(USER_PASSWORD)

    class Meta:
        model = models.User


class StaffFactory(BaseFactory):
    class Meta:
        model = models.Staff
