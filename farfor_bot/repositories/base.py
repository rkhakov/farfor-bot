import typing as t

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from farfor_bot.database.core import Base


Model = t.TypeVar("Model", bound=Base)
CreateSchema = t.TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = t.TypeVar("UpdateSchema", bound=BaseModel)


class BaseRepository(t.Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: t.Type[Model]):
        self.model = model

    def all(self, db: Session, *, skip: int = 0, limit: int = 100) -> t.List[Model]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get(self, db: Session, id: t.Any) -> t.Optional[Model]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_schema: CreateSchema) -> Model:
        obj_data = jsonable_encoder(obj_schema)
        db_obj = self.model(**obj_data)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(self, db: Session, *, db_obj: Model, obj_schema: UpdateSchema) -> Model:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_schema.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj

    def delete(self, db: Session, *, id: int) -> t.Optional[Model]:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return None

        db.delete(db_obj)
        db.commit()

        return db_obj
