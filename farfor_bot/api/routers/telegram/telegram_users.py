from farfor_bot.models.telegram_user import TelegramUser
from farfor_bot.schemas.telegram_user import TelegramUserUpdateSchema
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from farfor_bot.schemas import TelegramUserSchema, TelegramUserUpdateSchema
from farfor_bot.models import User
from farfor_bot.api.dependencies import get_db, get_admin_or_superuser
from farfor_bot.repositories import telegram_user_repository


router = APIRouter()


@router.get("/", response_model=List[TelegramUserSchema])
def get_telegram_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_admin_or_superuser),
):
    return telegram_user_repository.all(db, skip=skip, limit=limit)


@router.post("/", response_model=TelegramUserSchema)
def create_telegram_user(
    obj_schema: TelegramUserSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_or_superuser),
):
    if telegram_user_repository.get_by_user_id(db, user_id=obj_schema.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь телеграм с id {obj_schema.user_id} уже существует"
        )
    return telegram_user_repository.create(db, obj_schema=obj_schema)


@router.get("/{user_id}", response_model=TelegramUserSchema)
def get_telegram_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_or_superuser),
):
    telegram_user = telegram_user_repository.get(db, id=user_id)
    if not telegram_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь телеграм с id {user_id} уже существует",
        )
    return telegram_user


@router.put("/{user_id}", response_model=TelegramUserSchema)
def update_telegram_user(
    user_id: int,
    obj_schema: TelegramUserUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_or_superuser),
):
    telegram_user = telegram_user_repository.get(db, id=user_id)
    if not telegram_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Телеграм пользователь не найден",
        )

    telegram_user = telegram_user_repository.update(db, db_obj=telegram_user, obj_schema=obj_schema)
    return telegram_user


@router.delete("/{user_id}", response_model=TelegramUserSchema)
def delete_telegram_user(
    user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_admin_or_superuser)
):
    telegram_user = telegram_user_repository.get(db, id=user_id)
    if not telegram_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Телеграм пользователь не найден",
        )
        
    telegram_user = telegram_user_repository.delete(db, id=user_id)
    return telegram_user

