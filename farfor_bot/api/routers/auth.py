from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from farfor_bot.api.dependencies import get_db, get_user
from farfor_bot.models import User
from farfor_bot.repositories import user_repository
from farfor_bot.schemas import UserSchema
from farfor_bot.secutiry import create_access_token
from farfor_bot.config import settings

router = APIRouter()


class TokenSchema(BaseModel):
    access_token: str


@router.post("/login", response_model=TokenSchema)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    
    user = user_repository.authenticate(
        db, login=form_data.username, password=form_data.password
    )
    
    if not user:
        raise HTTPException(status_code=400, detail="Неправильный логин или пароль")
    
    if not user_repository.is_active(user):
        raise HTTPException(status_code=400, detail="Пользовател деактивирован")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id, expires_delta=access_token_expires)
    return {"access_token": access_token}


@router.post("/verify-token", response_model=UserSchema)
def verify_token(current_user: User = Depends(get_user)):
    return current_user
