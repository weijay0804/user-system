from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """
        擁有 Create, Read, Update, Delete (CRUD) 的物件

        Args:
            * `model`: A SQLAlchemy model class
            * `schema`: A Pydantic model class
        """

        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:

        return db.get(self.model, id)

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:

        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:

        objin_data = obj_in.model_dump()

        db_obj = self.model(**objin_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """支援使用 `UpdateSchemaType` 或 dict 的方式更新

        例如：
        ```python

            dict_data = {"id" : 1, "username" : "user1"}
            model_data = UpdateSchemaType(id=1, username="user1")
        ```
        """

        if isinstance(obj_in, dict):
            update_data = obj_in
            obj_data = obj_in

        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            obj_data = obj_in.model_dump()

        for field in update_data:

            if field in obj_data and update_data[field] is not None:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(self, db: Session, *, id: Any) -> None:

        obj = db.get(self.model, id)

        if obj:
            db.delete(obj)
            db.commit()
