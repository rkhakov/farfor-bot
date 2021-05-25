from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl, BaseModel, Field
from sqlalchemy.orm import Session

from farfor_bot.config import settings
from farfor_bot.models import User
from farfor_bot.services import telegram_service
from farfor_bot.api.dependencies import get_db, get_superuser


router = APIRouter()


class UserSchema(BaseModel):
    id: int
    first_name: str
    username: str


class MessageSchema(BaseModel):
    message_id: int
    text: str
    from_user: UserSchema = Field(alias="from")


class WerbhookSchema(BaseModel):
    update_id: int
    message: MessageSchema
    
    class Config:
        schema_extra = {
            "update_id": 434768931,
            "message": {
                "from": {
                    "id": 475516545,
                    "first_name": "Руслан",
                    "username": "rkhakov",
                },
                "text": "/start",
            },
        }


@router.post("/{telegram_token}")
async def webhook(telegram_token: str, webhook_schema: WerbhookSchema):
    if telegram_token != settings.TELEGRAM_TOKEN:
        raise HTTPException(status_code=401, detail="Некорректный токен")

    return {"success": True}


@router.put("/")
def set_webhook_url(domain: HttpUrl, current_user: User = Depends(get_superuser)):
    url = f'{domain}/api/telegram/webhook/{settings.TELEGRAM_TOKEN}'
    result = telegram_service.set_webhook(url)
    return {"success": result}


@router.get("/")
def get_webhook_url(current_user: User = Depends(get_superuser)):
    webhook_info = telegram_service.get_webhook_info()
    return {"webhook_url": webhook_info.url}


@router.delete("/")
def delete_webhook_url(current_user: User = Depends(get_superuser)):
    result = telegram_service.delete_webhook()
    return {"success": result}
