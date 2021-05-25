from sqlalchemy import Column, Integer, String, SmallInteger, Boolean

from farfor_bot.database.core import Base


class TelegramUser(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)
    name = Column(String)
    staff_city_id = Column(SmallInteger, index=True, nullable=False)
    staff_point_id = Column(SmallInteger, index=True, nullable=False)
    staff_module = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
