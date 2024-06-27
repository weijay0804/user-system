import logging
from datetime import datetime, timedelta

from fastapi import BackgroundTasks, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import security
from app.config.settings import get_settings
from app.crud import user_crud, user_token_crud
from app.models.user import User
from app.schemas import db_schemas, request_schemas, response_schemas
from app.security import (
    generate_token,
    get_token_payload,
    get_unique_string,
    str_decode,
    str_encode,
    verify_password,
)
from app.services.email import (
    send_account_verifiaction_confirmation_email,
    send_account_verification_email,
    send_password_reset_email,
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


def _generate_token(user: User, session: Session) -> response_schemas.JWTokenResp:

    refresh_key = get_unique_string(100)
    access_key = get_unique_string(50)
    rt_expires = timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token_in = db_schemas.UserTokenDBCreate(
        user_id=user.id,
        access_key=access_key,
        refresh_key=refresh_key,
        expires_at=datetime.now() + rt_expires,
    )

    # 讓 user 和 token 是一對一的關係
    # 這邊採取更新原有的 token 而不是再建立一筆新的 token
    # 為了防止如果用戶重新登入，而舊的那個 access token 還可以繼續使用
    if user.token:
        user_token = user_token_crud.update(session, db_obj=user.token, obj_in=user_token_in)

    else:
        user_token = user_token_crud.create(session, obj_in=user_token_in)

    at_payload = {
        "sub": str_encode(str(user.id)),
        "a": access_key,
        "r": str_encode(str(user_token.id)),
        "n": str_encode(user.name),
        "ty": str_encode("at"),
    }

    at_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(
        at_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, expiry=at_expires
    )

    rt_payload = {
        "sub": str_encode(str(user.id)),
        "t": refresh_key,
        "a": access_key,
        "ty": str_encode("rt"),
    }

    refresh_token = generate_token(
        rt_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, rt_expires
    )

    return response_schemas.JWTokenResp(
        access_token=access_token, refresh_token=refresh_token, expires_at=at_expires.seconds
    )


def get_login_token(
    data: OAuth2PasswordRequestForm, session: Session
) -> response_schemas.JWTokenResp:

    # 這邊的 username 等同於 email
    user = user_crud.get_by_email(session, email=data.username)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account is not active.")

    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is not verified.")

    return _generate_token(user, session)


def refresh_token(refresh_token: str, session: Session) -> response_schemas.JWTokenResp:

    token_payload = get_token_payload(refresh_token, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    if not token_payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")

    token_type = str_decode(token_payload.get("ty"))

    if token_type != "rt":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")

    user_id = str_decode(token_payload.get("sub"))

    user = user_crud.get(session, id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.")

    user_token = user.token

    if not user_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.")

    rt_key = token_payload.get("t")
    at_key = token_payload.get("a")

    if rt_key != user_token.refresh_key or at_key != user_token.access_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.")

    is_expires = user_token.expires_at < datetime.now()

    if is_expires:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired.")

    return _generate_token(user, session)


async def reset_password(
    data: request_schemas.UserResetPasswordReq,
    user: User,
    session: Session,
    bakground_tasks: BackgroundTasks,
):

    update_scheam = db_schemas.UserDBUpdate(password=security.hash_password(data.new_password))

    user_crud.update(session, db_obj=user, obj_in=update_scheam)

    await send_password_reset_email(user, bakground_tasks)
