from typing import List

from fastapi import APIRouter, Depends
from pydantic import AnyHttpUrl, BaseModel
from sqlalchemy.orm import Session

from farfor_bot.api.dependencies import get_db
from farfor_bot.repositories import staff_repository
from farfor_bot.services import telegram_service


router = APIRouter()


class CameraEvent(BaseModel):
    order_id: int
    usernames: List[str]
    station: str
    snapshot_url: AnyHttpUrl


class ResponseSchema(BaseModel):
    success: bool


@router.post("/camera_event", response_model=ResponseSchema)
def camera_event(event: CameraEvent, db: Session = Depends(get_db)):
    caption = f"Заказ: {event.order_id}\nСтанция: {event.station}"

    staff_objects = staff_repository.get_by_erp_usernames(
        db, erp_usernames=event.usernames
    )

    for staff in staff_objects:
        telegram_service.send_photo(staff.chat_id, event.snapshot_url, caption)
    return {"success": True}
