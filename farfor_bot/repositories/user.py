from typing import Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from farfor_bot.models import User
from farfor_bot.schemas import UserCreateSchema, UserUpdateSchema
from farfor_bot.secutiry import get_password_hash, verify_password

from .base import BaseRepository


class UserRepository(BaseRepository[User, UserCreateSchema, UserUpdateSchema]):
    def get_by_login(self, db: Session, *, login: str) -> Optional[User]:
        return db.query(User).filter(User.login == login).first()
    
    def create(self, db: Session, *, obj_schema: UserCreateSchema) -> User:
        db_obj = User(
            login=obj_schema.login,
            hashed_password=get_password_hash(obj_schema.password),
            first_name=obj_schema.first_name,
            last_name=obj_schema.last_name,
            is_admin=obj_schema.is_admin,
            is_superuser=obj_schema.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: User, obj_schema: UserUpdateSchema) -> User:
        update_data = obj_schema.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        obj_data = jsonable_encoder(db_obj)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    def authenticate(self, db: Session, *, login: str, password: str) -> Optional[User]:
        user = self.get_by_login(db, login=login)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        return user.is_active
    
    def is_admin(self, user: User) -> bool:
        return user.is_admin
    
    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user_repository = UserRepository(User)
