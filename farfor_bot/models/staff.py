from sqlalchemy import Column, Integer, String, SmallInteger, Boolean

from farfor_bot.database.core import Base


class Staff(Base):
    """Сотрудники из ERP с привязкой к телеграм боту по id чата"""

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    erp_username = Column(String)
    name = Column(String)
    city_id = Column(SmallInteger, nullable=False)
    point_id = Column(SmallInteger, index=True, nullable=False)
    module = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
