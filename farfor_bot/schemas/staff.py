from typing import Optional

from pydantic import BaseModel


class StaffBaseSchema(BaseModel):
    name: Optional[str] = None
    erp_username: Optional[str] = None
    city_id: int
    point_id: int
    module: str
    is_active: bool = True


class StaffCreateSchema(StaffBaseSchema):
    chat_id: int
    erp_username: str


class StaffUpdateSchema(StaffBaseSchema):
    pass


class StaffSchema(StaffBaseSchema):
    id: int
    chat_id: int

    class Config:
        orm_mode = True
