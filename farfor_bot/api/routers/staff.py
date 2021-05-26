from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from farfor_bot.api.dependencies import get_admin_or_superuser, get_db
from farfor_bot.repositories import staff_repository
from farfor_bot.schemas import StaffCreateSchema, StaffSchema, StaffUpdateSchema


router = APIRouter(dependencies=[Depends(get_admin_or_superuser)])


@router.get("/", response_model=List[StaffSchema])
def get_staff_list(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return staff_repository.all(db, skip=skip, limit=limit)


@router.post("/", response_model=StaffSchema)
def create_staff(staff_schema: StaffCreateSchema, db: Session = Depends(get_db)):
    if staff_repository.get_by_chat_id(db, chat_id=staff_schema.chat_id):
        error = f"Сотрудник с ID телеграм чата {staff_schema.chat_id} уже существует"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return staff_repository.create(db, obj_schema=staff_schema)


@router.get("/{staff_id}", response_model=StaffSchema)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = staff_repository.get(db, id=staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сотрудник с id {staff_id} не найден",
        )
    return staff


@router.put("/{staff_id}", response_model=StaffSchema)
def update_staff(
    staff_id: int,
    obj_schema: StaffUpdateSchema,
    db: Session = Depends(get_db),
):
    staff = staff_repository.get(db, id=staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сотрудник не найден",
        )

    staff = staff_repository.update(db, db_obj=staff, obj_schema=obj_schema)
    return staff


@router.delete("/{staff_id}", response_model=StaffSchema)
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = staff_repository.get(db, id=staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Телеграм пользователь не найден",
        )

    staff = staff_repository.delete(db, id=staff_id)
    return staff
