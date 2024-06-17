import logging
from datetime import datetime

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from app import security
from app.config.settings import get_settings
from app.crud import user_crud
from app.models.user import User
from app.schemas import db_schemas, request_schemas
from app.security import verify_password
from app.services.email import (
    send_account_verifiaction_confirmation_email,
    send_account_verification_email,
)

settings = get_settings()


async def create_user_account(
    data: request_schemas.UserCreateAccountResp, session: Session, backgroundtasks: BackgroundTasks
) -> User:

    user_exist = user_crud.get_by_email(session, email=data.email)

    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already exists.")

    hashed_pwd = security.hash_password(data.password)
    obj_in = db_schemas.UserDBCreate(email=data.email, name=data.name, password=hashed_pwd)

    user = user_crud.create(session, obj_in=obj_in)

    await send_account_verification_email(user=user, background_tasks=backgroundtasks)

    return user


async def activate_user_account(
    data: request_schemas.UserVerifiyAccountReq, session: Session, backgroundtasks: BackgroundTasks
) -> None:

    user = user_crud.get_by_email(session, email=data.email)

    if not user:
        raise HTTPException(status_code=400, detail="This link is not valid.")

    user_token = user.get_context_string(settings.USER_VERIFY_ACCOUNT_EMAIL_CONTEXT)

    try:
        token_valid = verify_password(user_token, data.token)

    except Exception as verify_exec:
        logging.exception(verify_exec)
        token_valid = False

    if not token_valid:
        raise HTTPException(status_code=400, detail="This link is not valid.")

    user.is_active = True
    user.updated_at = datetime.now()
    user.verified_at = datetime.now()

    session.add(user)
    session.commit()

    await send_account_verifiaction_confirmation_email(user, backgroundtasks)
