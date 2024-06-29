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
from app.services import email_serv

settings = get_settings()


async def activate_user_account(
    data: request_schemas.UserVerifiyAccountReq, session: Session, backgroundtasks: BackgroundTasks
) -> None:
    """認證使用者帳號，並發送帳號已啟用 email 至使用者信箱"""

    user = user_crud.get_by_email(session, email=data.email)

    if not user:
        raise HTTPException(status_code=400, detail="This link is not valid.")

    user_token = user.get_context_string(settings.USER_VERIFY_ACCOUNT_EMAIL_CONTEXT)

    try:
        token_valid = security.verify_hashed_string(user_token, data.token)

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

    await email_serv.send_account_verifiaction_confirmation_email(user, backgroundtasks)


def _generate_token(user: User, session: Session) -> response_schemas.JWTokenResp:
    """生成 JWT 並將 token 資料儲存至資料庫"""

    refresh_key = security.get_unique_string(100)
    access_key = security.get_unique_string(50)
    rt_expires = timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token_in = db_schemas.UserTokenDBCreate(
        user_id=user.id,
        access_key=access_key,
        refresh_key=refresh_key,
        expires_at=datetime.now() + rt_expires,
    )

    # TODO 這邊要改成一對多的關係
    # TODO 因為可能會有多個裝置使用的關係
    # 讓 user 和 token 是一對一的關係
    # 這邊採取更新原有的 token 而不是再建立一筆新的 token
    # 為了防止如果用戶重新登入，而舊的那個 access token 還可以繼續使用
    if user.token:
        user_token = user_token_crud.update(session, db_obj=user.token, obj_in=user_token_in)

    else:
        user_token = user_token_crud.create(session, obj_in=user_token_in)

    # TODO 這邊改成用 BaseModel
    at_payload = {
        "sub": security.str_encode(str(user.id)),
        "a": access_key,
        "r": security.str_encode(str(user_token.id)),
        "n": security.str_encode(user.name),
        "ty": security.str_encode("at"),
    }

    at_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.generate_token(
        at_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, expiry=at_expires
    )

    # TODO 這邊改成用 BaseModel
    rt_payload = {
        "sub": security.str_encode(str(user.id)),
        "t": refresh_key,
        "a": access_key,
        "ty": security.str_encode("rt"),
    }

    refresh_token = security.generate_token(
        rt_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, rt_expires
    )

    return response_schemas.JWTokenResp(
        access_token=access_token, refresh_token=refresh_token, expires_at=at_expires.seconds
    )


def get_login_token(
    data: OAuth2PasswordRequestForm, session: Session
) -> response_schemas.JWTokenResp:
    """使用者登入，並回傳 JWT

    `data` 中的 `username` 等同於 `email`

    """

    # 這邊的 username 等同於 email
    user = user_crud.get_by_email(session, email=data.username)

    if not user or not security.verify_hashed_string(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account is not active.")

    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is not verified.")

    return _generate_token(user, session)


def refresh_token(refresh_token: str, session: Session) -> response_schemas.JWTokenResp:
    """使用 refresh token 取得新的 access token"""

    token_payload = security.get_token_payload(
        refresh_token, settings.JWT_SECRET, settings.JWT_ALGORITHM
    )

    if not token_payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")

    token_type = security.str_decode(token_payload.get("ty"))

    if token_type != "rt":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")

    user_id = security.str_decode(token_payload.get("sub"))

    user = user_crud.get(session, id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.")

    user_token = user.token

    if not user_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.")

    # 這邊檢查傳入的 token type 是不是 `refresh token`
    rt_key = token_payload.get("t")
    at_key = token_payload.get("a")

    if rt_key != user_token.refresh_key or at_key != user_token.access_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.")

    is_expires = user_token.expires_at < datetime.now()

    if is_expires:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired.")

    return _generate_token(user, session)


async def forgot_password(
    data: request_schemas.UserForgotPasswordReq, session: Session, bakground_tasks: BackgroundTasks
):
    """使用者忘記密碼的請求，會發送重新設定密碼的 email 至使用者信箱"""

    user = user_crud.get_by_email(session, email=data.email)

    if user is None:
        raise HTTPException(status_code=400, detail="Email is not exists.")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account is not active.")

    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is not verified.")

    await email_serv.send_forgot_password_reset_email(user, bakground_tasks)


async def forgot_password_reset(
    data: request_schemas.UserForgotPasswordResetReq,
    background_tasks: BackgroundTasks,
    session: Session,
):
    """使用者重新設定密碼，這個函數是針對未登入的使用者，並會在重新設定密碼後發送密碼已經被重新設定的 email 至使用者信箱"""

    user = user_crud.get_by_email(session, email=data.email)

    if not user:
        raise HTTPException(status_code=400, detail="Email is not exists.")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account is not active.")

    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is not verified.")

    user_token = user.get_context_string(settings.USER_FORGOT_PASSWORD_EMAIL_CONTEXT)

    try:
        token_valid = security.verify_hashed_string(user_token, data.token)

    except Exception as verify_exec:
        logging.exception(verify_exec)
        token_valid = False

    if not token_valid:
        raise HTTPException(status_code=400, detail="This link is not valid.")

    update_scheam = db_schemas.UserDBUpdate(
        password=security.verify_hashed_string(data.new_password)
    )

    user_crud.update(session, db_obj=user, obj_in=update_scheam)

    await email_serv.send_password_reset_email(user, background_tasks)
