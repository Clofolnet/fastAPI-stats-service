from typing import Any, Generic, List, Optional, Type, TypeVar

from db.base_class import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text as sqlalchemy_text
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def _get_model(self, obj_in: CreateSchemaType):
        obj_in_data = jsonable_encoder(obj_in)
        return self.model(**obj_in_data)

    def bulk_create(self, db: Session, *, objs: List[CreateSchemaType]) -> List[ModelType]:
        models = [self._get_model(i) for i in objs]
        db.bulk_save_objects(models)
        db.commit()
        return models

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).filter_by(id=id).first()
        db.delete(obj)
        db.commit()
        return obj

    def delete_all(self, db: Session) -> None:
        db.execute(sqlalchemy_text(
            f"TRUNCATE TABLE {self.model.__tablename__}"))
        db.commit()
