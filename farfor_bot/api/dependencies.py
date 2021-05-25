from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError
from sqlalchemy.orm.session import Session
from jose import jwt
from starlette.status import HTTP_400_BAD_REQUEST

from farfor_bot.config import settings
from farfor_bot.database.core import SessionLocal
from farfor_bot.models import User
from farfor_bot.repositories import user_repository
from farfor_bot.schemas import TokenPayload
from farfor_bot.secutiry import ALGORITHM


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/auth/access-token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не удалось проверить токен",
        )
        
    user = user_repository.get(db, id=token_data.user_id)
    
    if not user or not user_repository.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    return user


def get_admin(user: User = Depends(get_user)):
    if not user_repository.is_admin(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно прав")
    return user


def get_superuser(user: User = Depends(get_user)):
    if not user_repository.is_superuser(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно прав")
    return user

