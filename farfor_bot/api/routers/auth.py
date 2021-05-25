from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from farfor_bot.api.dependencies import get_db
from farfor_bot.schemas import TokenSchema
from farfor_bot.repositories import user_repository
from farfor_bot.secutiry import create_access_token
from farfor_bot.config import settings

router = APIRouter()


@router.post("/access-token", response_model=TokenSchema)
def access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    
    user = user_repository.authenticate(
        db, login=form_data.username, password=form_data.password
    )
    
    if not user:
        raise HTTPException(status_code=400, detail="Неправильный логин или пароль")
    
    if not user_repository.is_active(user):
        raise HTTPException(status_code=400, detail="Пользовател деактивирован")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
