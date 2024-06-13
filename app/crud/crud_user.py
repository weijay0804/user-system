from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas import db_schemas


class UserCRUD(CRUDBase[User, db_schemas.UserDBCreate, db_schemas.UserDBUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:

        return db.query(self.model).filter(self.model.email == email).first()


user_crud = UserCRUD(User)
