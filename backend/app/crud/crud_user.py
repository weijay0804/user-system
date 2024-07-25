from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.user import User, UserToken
from app.schemas import db_schemas


class UserCRUD(CRUDBase[User, db_schemas.user.UserDBCreate, db_schemas.user.UserDBUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:

        return db.query(self.model).filter(self.model.email == email).first()


class UserTokenCRUD(
    CRUDBase[UserToken, db_schemas.user.UserTokenDBCreate, db_schemas.user.UserTokenDBUpdate]
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

    def get_by_key(self, db: Session, *, token_key: str) -> Optional[UserToken]:

        return db.query(self.model).filter(self.model.token_key == token_key).first()

    def clear_up_expired_tokens(self, db: Session, *, user_id: int) -> None:
        """清除過期的 token"""

        # 為了能夠比對 datetime 的值，需把 timezone 設為 None
        db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.expires_at < datetime.now(timezone.utc).replace(tzinfo=None),
        ).delete()

        db.commit()


user_crud = UserCRUD(User)
user_token_crud = UserTokenCRUD(UserToken)
