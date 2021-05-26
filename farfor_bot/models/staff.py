from sqlalchemy import Boolean, Column, Integer, String

from farfor_bot.database.core import Base


class Staff(Base):
    """Сотрудники из ERP с привязкой к телеграм боту по id чата"""

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    erp_username = Column(String, index=True)
    name = Column(String)
    is_active = Column(Boolean(), default=True)
