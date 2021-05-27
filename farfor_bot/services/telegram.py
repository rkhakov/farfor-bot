import logging

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from telegram import Bot
from telegram.error import TelegramError

from farfor_bot.config import settings


logger = logging.getLogger(__name__)
bot = Bot(token=settings.TELEGRAM_TOKEN)


def send_photo(chat_id: int, photo_url: str, caption: str):
    bot.send_photo(chat_id=chat_id, photo=photo_url, caption=caption)


def send_message(chat_id: int, message: str):
    bot.send_message(chat_id=chat_id, text=message)


class WebhookInfoSchema(BaseModel):
    url: str


def get_webhook_info() -> WebhookInfoSchema:
    webhook_info_data = jsonable_encoder(bot.get_webhook_info())
    return WebhookInfoSchema(**webhook_info_data)


def set_webhook(url: str):
    try:
        return bot.set_webhook(str(url))
    except TelegramError:
        logger.exception("Ошибка установки вебхука телеграм бота")
        return False


def delete_webhook():
    return bot.delete_webhook()
