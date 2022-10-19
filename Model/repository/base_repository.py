from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from fastapi.encoders import jsonable_encoder

from Model.database.settings import get_db
from Controller.exceptions import APIException


ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""
        self.model = model
        self.db = next(get_db())

    def get(self, uid: Any) -> Optional[ModelType]:
        try:
            result = self.db.query(self.model).filter(self.model.id == uid).first()
        except Exception as e:
            self.db.rollback()
            raise APIException(e.args) from e
        return result

    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        try:
            result = self.db.query(self.model).offset(skip).limit(limit).all()
        except Exception as e:
            self.db.rollback()
            raise APIException(e.args) from e
        return result

    def create(self, obj: dict) -> ModelType:
        try:
            db_obj = self.model(**obj)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        except Exception as e:
            self.db.rollback()
            raise APIException(e.args) from e
        return db_obj

    def bulk_insert(self, objects: List):
        try:
            self.db.add_all(objects)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise APIException(e.args) from e
        return True

    def update(self, db_obj: ModelType, fields: Dict[str, Any]) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)
            for field in obj_data:
                if field in fields:
                    setattr(db_obj, field, fields[field])
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        except Exception as e:
            self.db.rollback()
            raise APIException(e.args) from e
        return db_obj

    def remove(self, model_id: int) -> ModelType:
        try:
            obj = self.db.query(self.model).get(model_id)
            self.db.delete(obj)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise APIException(e.args) from e
        return True
