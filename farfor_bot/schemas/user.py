from typing import Optional

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    login: str

    is_active: Optional[bool] = True
    is_superuser: bool = False
    is_admin: bool = False

    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreateSchema(UserBaseSchema):
    login: str
    password: str


class UserUpdateSchema(UserBaseSchema):
    password: Optional[str] = None


class UserInDBBaseSchema(UserBaseSchema):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserSchema(UserInDBBaseSchema):
    pass


class UserInDBSchema(UserInDBBaseSchema):
    hashed_password: str
