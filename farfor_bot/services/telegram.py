from telegram import Bot
from pydantic import HttpUrl, BaseModel
from fastapi.encoders import jsonable_encoder

from farfor_bot.config import settings


bot = Bot(token=settings.TELEGRAM_TOKEN)


def send_photo(chat_id: int, photo_url: HttpUrl, caption: str):
    bot.send_photo(chat_id=chat_id, photo=photo_url, caption=caption)
    
    
class WebhookInfo(BaseModel):
    url: str


def get_webhook_info() -> WebhookInfo:
    webhook_info_data = jsonable_encoder(bot.get_webhook_info())
    return WebhookInfo(**webhook_info_data)


def set_webhook(url: HttpUrl):
    return bot.set_webhook(str(url))


def delete_webhook():
    return bot.delete_webhook()
