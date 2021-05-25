from telegram import Bot
from pydantic import HttpUrl, BaseModel
from fastapi.encoders import jsonable_encoder

from farfor_bot.config import settings


bot = Bot(token=settings.TELEGRAM_TOKEN)


def send_photo(chat_id: int, photo_url: HttpUrl, caption: str):
    bot.send_photo(chat_id=chat_id, photo=photo_url, caption=caption)
    
    
def send_message(chat_id: int, message: str):
    bot.send_message(chat_id=chat_id, text=message)
    
    
class WebhookInfoSchema(BaseModel):
    url: str


def get_webhook_info() -> WebhookInfoSchema:
    webhook_info_data = jsonable_encoder(bot.get_webhook_info())
    return WebhookInfoSchema(**webhook_info_data)


def set_webhook(url: HttpUrl):
    return bot.set_webhook(str(url))


def delete_webhook():
    return bot.delete_webhook()
