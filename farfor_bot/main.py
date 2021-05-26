"""Входная точка для запуска FastAPI приложения"""
from fastapi import FastAPI

from farfor_bot.api.routers import api_router
from farfor_bot.config import settings


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router)
