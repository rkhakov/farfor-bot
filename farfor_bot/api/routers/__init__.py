from fastapi import APIRouter

from . import webhook


api_router = APIRouter(prefix="/api")
api_router.include_router(webhook.router, prefix="/telegram", tags=["telegram"])