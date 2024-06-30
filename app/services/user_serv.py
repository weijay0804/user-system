from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from app import security
from app.config.settings import get_settings
from app.crud import crud_user
from app.models.user import User
from app.schemas import db_schemas, request_schemas
from app.services import email_serv

settings = get_settings()


async def create_user_account(
    data: request_schemas.user.UserCreateAccountReq,
    session: Session,
    backgroundtasks: BackgroundTasks,
) -> User:
    """建立使用者帳戶，並發送認證帳戶的 email 至使用者信箱"""

    user_exist = crud_user.user_crud.get_by_email(session, email=data.email)

    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already exists.")

    hashed_pwd = security.hash_string(data.password)
    obj_in = db_schemas.user.UserDBCreate(email=data.email, name=data.name, password=hashed_pwd)

    user = crud_user.user_crud.create(session, obj_in=obj_in)

    await email_serv.send_account_verification_email(user=user, background_tasks=backgroundtasks)

    return user


async def reset_password(
    data: request_schemas.user.UserResetPasswordReq,
    user: User,
    session: Session,
    bakground_tasks: BackgroundTasks,
):
    """使用者重新設定密碼，這個函數是針對已經登入的使用者，並會在重新設定密碼後發送密碼已經被重新設定的 email 至使用者信箱"""

    update_scheam = db_schemas.user.UserDBUpdate(password=security.hash_string(data.new_password))

    crud_user.user_crud.update(session, db_obj=user, obj_in=update_scheam)

    await email_serv.send_password_reset_email(user, bakground_tasks)
