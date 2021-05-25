from fastapi import APIRouter

from . import telegram_users
from . import webhook


api_router = APIRouter()
api_router.include_router(telegram_users.router, prefix="/users")
api_router.include_router(webhook.router, prefix="/webhook")
