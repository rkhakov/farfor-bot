from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy.orm import Session

from farfor_bot.api.dependencies import get_db, get_superuser
from farfor_bot.config import settings
from farfor_bot.repositories import staff_repository
from farfor_bot.schemas import StaffCreateSchema
from farfor_bot.services import telegram_service


router = APIRouter()


class FromChatSchema(BaseModel):
    id: int
    first_name: str
    username: str


class MessageSchema(BaseModel):
    message_id: int
    text: str
    from_chat: FromChatSchema = Field(alias="from")


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


@router.post("/{telegram_token}", responses={200: {"model": ResponseSchema}})
async def webhook(
    telegram_token: str,
    webhook_schema: WebhookSchema,
    db: Session = Depends(get_db),
):
    if telegram_token != settings.TELEGRAM_TOKEN:
        raise HTTPException(status_code=401, detail="Некорректный токен")

    if webhook_schema.message.text != "/start":
        return JSONResponse(content={"success": True})

    from_chat = webhook_schema.message.from_chat
    telegram_user = staff_repository.get_by_chat_id(db, chat_id=from_chat.id)
    if telegram_user:
        return JSONResponse(content={"success": True})

    staff_schema = StaffCreateSchema(
        name=from_chat.first_name,
        erp_username="NULL",  # будет устанавливаться вручную
        chat_id=from_chat.id,
    )

    staff_repository.create(db, obj_schema=staff_schema)

    message = f"""{staff_schema.name}, добро пожаловать в Фарфор Бот
Ваш ID: {staff_schema.chat_id}
Для подключения к боту, обратитесь в техподдержку, сообщив им Ваш ID и логин в ERP
"""
    telegram_service.send_message(chat_id=staff_schema.chat_id, message=message)
    return JSONResponse(content={"success": True})


@router.put("/", dependencies=[Depends(get_superuser)])
def set_webhook_url(domain: HttpUrl):
    url = f"{domain}/api/webhook/{settings.TELEGRAM_TOKEN}"
    result = telegram_service.set_webhook(url)
    return {"success": result}


@router.get("/", dependencies=[Depends(get_superuser)])
def get_webhook_url():
    webhook_info = telegram_service.get_webhook_info()
    return {"webhook_url": webhook_info.url}


@router.delete("/", dependencies=[Depends(get_superuser)])
def delete_webhook_url():
    result = telegram_service.delete_webhook()
    return {"success": result}
