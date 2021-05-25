from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl, BaseModel, Field
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from farfor_bot.config import settings
from farfor_bot.models import User
from farfor_bot.services import telegram_service
from farfor_bot.schemas import TelegramUserCreateSchema
from farfor_bot.api.dependencies import get_db, get_superuser
from farfor_bot.repositories import telegram_user_repository


router = APIRouter()


class TgUserSchema(BaseModel):
    id: int
    first_name: str
    username: str


class MessageSchema(BaseModel):
    message_id: int
    text: str
    from_user: TgUserSchema = Field(alias="from")


class WebhookSchema(BaseModel):
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


class ResponseSchema(BaseModel):
    status: bool


@router.post(
    "/{telegram_token}",
    responses={200: {"model": ResponseSchema}}
)
async def webhook(
    telegram_token: str, 
    webhook_schema: WebhookSchema,
    db: Session = Depends(get_db)
):
    if telegram_token != settings.TELEGRAM_TOKEN:
        raise HTTPException(status_code=401, detail="Некорректный токен")
    
    if webhook_schema.message.text != "/start":
        return JSONResponse(content={"success": True})
    
    user_data = webhook_schema.message.from_user
    telegram_user = telegram_user_repository.get_by_user_id(db, user_id=user_data.id)
    if telegram_user:
        return JSONResponse(content={"success": True})
    
    tg_user_schema = TelegramUserCreateSchema(
        name=user_data.first_name,
        user_id=user_data.id,
        staff_city_id=0,
        staff_point_id=0,
        staff_module="manager",
    )

    telegram_user_repository.create(db, obj_schema=tg_user_schema)
    
    message = f"""{tg_user_schema.name}, добро пожаловать в Фарфор Бот
Ваш ID: {tg_user_schema.user_id}
Для подключения к боту, обратитесь в техподдержку, сообщив им Ваш ID.
"""
    telegram_service.send_message(chat_id=tg_user_schema.user_id, message=message)
    return JSONResponse(content={"success": True})


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
