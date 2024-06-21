from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User, UserToken
from app.schemas import db_schemas


class UserCRUD(CRUDBase[User, db_schemas.UserDBCreate, db_schemas.UserDBUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:

        return db.query(self.model).filter(self.model.email == email).first()


class UserTokenCRUD(
    CRUDBase[UserToken, db_schemas.UserTokenDBCreate, db_schemas.UserTokenDBUpdate]
):

    pass


user_crud = UserCRUD(User)
user_token_crud = UserTokenCRUD(UserToken)
