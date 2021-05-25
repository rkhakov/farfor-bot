from typing import List
from farfor_bot.models import Staff
from farfor_bot.schemas import StaffCreateSchema, StaffUpdateSchema
from sqlalchemy.orm import Session

from .base import BaseRepository


class StaffRepository(BaseRepository[Staff, StaffCreateSchema, StaffUpdateSchema]):
    def get_manager_by_point_ids(self, db: Session, *, point_ids: List[int]):
        return db.query(Staff).filter(
            Staff.point_id.in_(point_ids),
            Staff.module == "manager",
        ).all()
        
    def get_by_chat_id(self, db: Session, *, chat_id: int):
        return db.query(Staff).filter(Staff.chat_id == chat_id).first()


staff_repository = StaffRepository(Staff)
