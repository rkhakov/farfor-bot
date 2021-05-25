from typing import Optional

from pydantic import BaseModel



class TelegramUserBaseSchema(BaseModel):
    name: Optional[str] = None
    staff_city_id: int
    staff_point_id: int
    staff_module: str
    is_active: bool = True
    
    class Config:
        orm_mode = True


class TelegramUserSchema(TelegramUserBaseSchema):
    id: int
    user_id: int
    

class TelegramUserUpdateSchema(TelegramUserBaseSchema):
    pass
