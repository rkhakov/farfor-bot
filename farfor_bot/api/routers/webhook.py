from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl, BaseModel, Field

from farfor_bot.config import settings
from farfor_bot.services import telegram_service



router = APIRouter()


class FromUser(BaseModel):
    id: int
    first_name: str
    username: str


class Message(BaseModel):
    message_id: int
    text: str
    from_user: FromUser = Field(alias="from")


class WebhookData(BaseModel):
    update_id: int
    message: Message
    
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


@router.post("/webhook/{telegram_token}")
async def webhook(telegram_token: str, webhook_data: WebhookData):
    if telegram_token != settings.TELEGRAM_TOKEN:
        raise HTTPException(status_code=401, detail="Некорректный токен")

    return {"success": True}


@router.put("/webhook")
def set_webhook_url(domain: HttpUrl):
    url = f'{domain}/api/telegram/webhook/{settings.TELEGRAM_TOKEN}'
    result = telegram_service.set_webhook(url)
    return {"success": result}


@router.get("/webhook")
def get_webhook_url():
    webhook_info = telegram_service.get_webhook_info()
    return {"webhook_url": webhook_info.url}


@router.delete("/webhook")
def delete_webhook_url():
    result = telegram_service.delete_webhook()
    return {"success": result}
