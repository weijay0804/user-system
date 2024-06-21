from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.user import User, UserToken
from app.schemas import db_schemas


class UserCRUD(CRUDBase[User, db_schemas.UserDBCreate, db_schemas.UserDBUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:

        return db.query(self.model).filter(self.model.email == email).first()


class UserTokenCRUD(
    CRUDBase[UserToken, db_schemas.UserTokenDBCreate, db_schemas.UserTokenDBUpdate]
):

    def get_user(self, db: Session, *, token_id: int, access_key: str, user_id: int) -> User:

        user_token = (
            db.query(self.model)
            .options(joinedload(UserToken.user))
            .filter(
                UserToken.id == token_id,
                UserToken.access_key == access_key,
                UserToken.user_id == user_id,
                UserToken.expires_at > datetime.now(),
            )
            .first()
        )

        if not user_token:
            return None

        return user_token.user


user_crud = UserCRUD(User)
user_token_crud = UserTokenCRUD(UserToken)
