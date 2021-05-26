from typing import List

from sqlalchemy.orm import Session

from farfor_bot.models import Staff
from farfor_bot.schemas import StaffCreateSchema, StaffUpdateSchema

from .base import BaseRepository


class StaffRepository(BaseRepository[Staff, StaffCreateSchema, StaffUpdateSchema]):
    def get_by_erp_usernames(self, db: Session, *, erp_usernames: List[str]):
        return db.query(Staff).filter(Staff.erp_username.in_(erp_usernames)).all()

    def get_by_chat_id(self, db: Session, *, chat_id: int):
        return db.query(Staff).filter(Staff.chat_id == chat_id).first()


staff_repository = StaffRepository(Staff)
