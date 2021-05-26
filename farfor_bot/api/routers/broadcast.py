from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, AnyHttpUrl
from sqlalchemy.orm import Session

from farfor_bot.api.dependencies import get_db
from farfor_bot.services import telegram_service
from farfor_bot.repositories import staff_repository


router = APIRouter()


class CameraEvent(BaseModel):
    order_id: int
    city_id: int
    point_ids: List[int]
    station: str
    snapshot_url: AnyHttpUrl


class ResponseSchema(BaseModel):
    success: bool


@router.post("/camera_event", response_model=ResponseSchema)
def camera_event(event: CameraEvent, db: Session = Depends(get_db)):
    caption = f"Заказ: {event.order_id}\nСтанция: {event.station}"

    staff_objects = staff_repository.get_manager_by_point_ids(
        db, point_ids=event.point_ids
    )

    for staff in staff_objects:
        telegram_service.send_photo(staff.chat_id, event.snapshot_url, caption)
    return {"success": True}
