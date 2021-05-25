from fastapi import APIRouter
from . import auth
from . import users
from . import webhook


api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(webhook.router, prefix="/telegram", tags=["telegram"])
