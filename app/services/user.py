from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import security
from app.crud import user_crud
from app.models.user import User
from app.schemas import db_schemas, request_schemas


def create_user_account(data: request_schemas.UserCreateAccountResp, session: Session) -> User:

    user_exist = user_crud.get_by_email(session, email=data.email)

    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already exists.")

    hashed_pwd = security.hash_password(data.password)
    obj_in = db_schemas.UserDBCreate(email=data.email, name=data.name, password=hashed_pwd)

    user = user_crud.create(session, obj_in=obj_in)

    return user
