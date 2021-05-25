from fastapi import APIRouter
from . import auth
from . import users
from . import staff
from . import webhook
from . import broadcast


api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(staff.router, prefix="/staff", tags=["staff"])
api_router.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
api_router.include_router(broadcast.router, prefix="/broadcast", tags=["broadcast"])
