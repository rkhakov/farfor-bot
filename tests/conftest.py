import pytest
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.config import environ

from farfor_bot.__main__ import ALEMBIC_PATH
from farfor_bot.config import settings
from farfor_bot.database.core import Base, SessionLocal, engine
from farfor_bot.main import app
from farfor_bot.security import get_password_hash
from tests.factories import StaffFactory, UserFactory


@pytest.fixture(scope="session", autouse=True)
def db():
    if not database_exists(settings.SQLALCHEMY_DATABASE_URI):
        create_database(settings.SQLALCHEMY_DATABASE_URI)

    Base.metadata.create_all(engine)
    alimbic_cfg = AlembicConfig(ALEMBIC_PATH)
    alembic_command.stamp(alimbic_cfg, "head")

    # db = SessionLocal()
    yield db
    drop_database(settings.SQLALCHEMY_DATABASE_URI)


@pytest.fixture(scope="function")
def session(db):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(scope="function")
def api_client(session):
    yield TestClient(app)


# register(UserFactory)
# register(StaffFactory)
