from typing import List
from farfor_bot.models import TelegramUser
from farfor_bot.schemas import TelegramUserSchema, TelegramUserUpdateSchema
from sqlalchemy.orm import Session

from .base import BaseRepository


class TelegramUserRepository(BaseRepository[TelegramUser, TelegramUserSchema, TelegramUserUpdateSchema]):
    def get_manager_by_point_ids(self, db: Session, *, point_ids: List[int]):
        return db.query(TelegramUser).filter(
            TelegramUser.staff_point_id.in_ == point_ids,
            TelegramUser.staff_module == "manager",
        ).all()
        
    def get_by_user_id(self, db: Session, *, user_id: int):
        return db.query(TelegramUser).filter(TelegramUser.user_id == user_id).first()


telegram_user_repository = TelegramUserRepository(TelegramUser)
