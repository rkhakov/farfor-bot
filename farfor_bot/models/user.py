from sqlalchemy import Boolean, Column, Integer, String

from farfor_bot.database.core import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)

    login = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String)
    last_name = Column(String)

    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
