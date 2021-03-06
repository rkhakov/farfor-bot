from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from farfor_bot.api.dependencies import get_db, get_superuser, get_user
from farfor_bot.models import User
from farfor_bot.repositories import user_repository
from farfor_bot.schemas import UserCreateSchema, UserSchema, UserUpdateSchema


router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def users_list(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_superuser),
):
    users = user_repository.all(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_schema: UserCreateSchema,
    current_user: User = Depends(get_superuser),
):
    user = user_repository.get_by_login(db, login=user_schema.login)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с логином {user_schema.login} уже существует",
        )

    user = user_repository.create(db, obj_schema=user_schema)
    return user


@router.get("/{user_id}", response_model=UserSchema)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user),
):
    user = user_repository.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    if user == current_user:
        return user

    if not user_repository.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно прав"
        )

    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_schema: UserUpdateSchema,
    current_user: User = Depends(get_user),
):
    user = user_repository.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    if user == current_user:
        user = user_repository.update(db, db_obj=user, obj_schema=user_schema)
        return user

    if not user_repository.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно прав"
        )

    user = user_repository.update(db, db_obj=user, obj_schema=user_schema)
    return user


@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_superuser),
):
    user = user_repository.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    if user == current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы не можете удалить своего пользователя",
        )

    user = user_repository.delete(db, id=user_id)
    return user
