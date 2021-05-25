from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError, BaseModel
from sqlalchemy.orm.session import Session
from jose import jwt

from farfor_bot.config import settings
from farfor_bot.database.core import SessionLocal
from farfor_bot.models import User
from farfor_bot.repositories import user_repository
from farfor_bot.secutiry import ALGORITHM


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/auth/login")


class TokenPayloadSchema(BaseModel):
    user_id: Optional[int] = None


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        # Декодируем токен
        # На выходе получим изначально закодированный дикт
        # {"exp": 1622646445, "user_id": 1}
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayloadSchema(**payload)
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


def get_admin_or_superuser(user: User = Depends(get_user)):
    if user_repository.is_admin(user):
        return user
    
    if user_repository.is_superuser(user):
        return user
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно прав")
