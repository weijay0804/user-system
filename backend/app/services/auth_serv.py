import logging
from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import BackgroundTasks, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import security
from app.config.settings import get_settings
from app.crud import crud_user
from app.models.user import User
from app.schemas import db_schemas, request_schemas, response_schemas, utils_schemas
from app.services import email_serv

settings = get_settings()


async def activate_user_account(
    data: request_schemas.user.UserVerifiyAccountReq,
    session: Session,
    backgroundtasks: BackgroundTasks,
) -> None:
    """認證使用者帳號，並發送帳號已啟用 email 至使用者信箱"""

    user = crud_user.user_crud.get_by_email(session, email=data.email)

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
    user.verified_at = datetime.now(timezone.utc)

    session.add(user)
    session.commit()

    await email_serv.send_account_verifiaction_confirmation_email(user, backgroundtasks)


async def resend_verifiy_email(
    data: request_schemas.auth.ReSendVerifiyEmailReq,
    background_tasks: BackgroundTasks,
    session: Session,
):
    """重新寄送用戶認證 email 至使用者信箱"""

    user = crud_user.user_crud.get_by_email(session, email=data.email)

    if not user:
        raise HTTPException(status_code=400, detail="Email is not exists.")

    if user.is_active or user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is already active.")

    await email_serv.send_account_verification_email(user, background_tasks)


def _generate_token_payload(
    user: User, purpose: Literal["at", "rt"]
) -> utils_schemas.jwt.JWTPayload:
    """生成 JWT payload

    `purpose` 為 `at` 代表 `access token`，`rt` 代表 `refresh token`

    """

    if purpose == "at":
        token_key = security.get_unique_string(50)
        expires_min = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    elif purpose == "rt":
        token_key = security.get_unique_string(100)
        expires_min = settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
    else:
        raise ValueError("Invalid token purpose.")

    expires = timedelta(minutes=expires_min)
    expires_at = datetime.now(timezone.utc) + expires

    token_payload = utils_schemas.jwt.JWTPayload(
        sub=security.str_encode(str(user.id)),
        t=token_key,
        p=security.str_encode(purpose),
        exp=expires_at,
    )

    return token_payload


def _generate_token(payload: utils_schemas.jwt.JWTPayload) -> response_schemas.auth.JWToken:
    """產生 JWT token"""

    token = security.generate_token(
        payload.model_dump(), settings.JWT_SECRET, settings.JWT_ALGORITHM
    )

    return response_schemas.auth.JWToken(token=token, expires_at=payload.exp)


def get_login_token(
    data: OAuth2PasswordRequestForm, session: Session
) -> response_schemas.auth.JWTokenResp:
    """使用者登入，並回傳 JWT

    `data` 中的 `username` 等同於 `email`

    並會將 refresh token 寫入資料庫

    並會清理資料庫中屬於該 user 的過期的 refresh token 資料

    """

    # 這邊的 username 等同於 email
    user = crud_user.user_crud.get_by_email(session, email=data.username)

    if not user or not security.verify_hashed_string(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account is not active.")

    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is not verified.")

    at_payload = _generate_token_payload(user, "at")
    rt_payload = _generate_token_payload(user, "rt")

    # 資料庫中只存 refresh token 資料
    rt_token_in = db_schemas.user.UserTokenDBCreate(
        user_id=user.id,
        token_key=rt_payload.t,
        expires_at=rt_payload.exp,
        purpose="rt",
    )

    crud_user.user_token_crud.create(session, obj_in=rt_token_in)

    at = _generate_token(at_payload)
    rt = _generate_token(rt_payload)

    crud_user.user_token_crud.clear_up_expired_tokens(session, user_id=user.id)

    return response_schemas.auth.JWTokenResp(access_token=at, refresh_token=rt)


def refresh_token(refresh_token: str, session: Session) -> response_schemas.auth.JWTokenResp:
    """使用 refresh token 取得新的 access token 和 refresh token

    如果 refresh token 有效，則會生成新的 access token 和 refresh token，並會將在資料庫中的 refresh token 更新，
    並清理資料庫中屬於該 user 的過期的 refresh token 資料
    """

    token_payload = security.get_token_payload(
        refresh_token, settings.JWT_SECRET, settings.JWT_ALGORITHM
    )

    # NOTE 這邊可以再重構一下
    if "error" in token_payload:
        if token_payload["error"] == "token expired":

            raise HTTPException(status_code=401, detail="Token expired.")

        if token_payload["error"] == "token invalid":
            raise HTTPException(status_code=401, detail="Not authorised.")

    payload_obj = utils_schemas.jwt.JWTPayload(**token_payload)

    token_type = security.str_decode(payload_obj.p)

    if token_type != "rt":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")

    user_id = security.str_decode(payload_obj.sub)

    user = crud_user.user_crud.get(session, id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.")

    token_key = payload_obj.t

    user_token = crud_user.user_token_crud.get_by_key(session, token_key=token_key)

    if not user_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request.")

    at_patload = _generate_token_payload(user, "at")
    rt_payload = _generate_token_payload(user, "rt")

    # 更新 token 資料，並清理過期的 token
    rt_token_update_in = db_schemas.user.UserTokenDBUpdate(
        token_key=rt_payload.t,
        expires_at=rt_payload.exp,
    )

    crud_user.user_token_crud.update(session, db_obj=user_token, obj_in=rt_token_update_in)
    crud_user.user_token_crud.clear_up_expired_tokens(session, user_id=user.id)

    at = _generate_token(at_patload)
    rt = _generate_token(rt_payload)

    return response_schemas.auth.JWTokenResp(access_token=at, refresh_token=rt)


async def forgot_password(
    data: request_schemas.user.UserForgotPasswordReq,
    session: Session,
    bakground_tasks: BackgroundTasks,
):
    """使用者忘記密碼的請求，會發送重新設定密碼的 email 至使用者信箱"""

    user = crud_user.user_crud.get_by_email(session, email=data.email)

    if user is None:
        raise HTTPException(status_code=400, detail="Email is not exists.")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account is not active.")

    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is not verified.")

    await email_serv.send_forgot_password_reset_email(user, bakground_tasks)


async def forgot_password_reset(
    data: request_schemas.user.UserForgotPasswordResetReq,
    background_tasks: BackgroundTasks,
    session: Session,
):
    """使用者重新設定密碼，這個函數是針對未登入的使用者，並會在重新設定密碼後發送密碼已經被重新設定的 email 至使用者信箱"""

    user = crud_user.user_crud.get_by_email(session, email=data.email)

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

    update_scheam = db_schemas.user.UserDBUpdate(password=security.hash_string(data.new_password))

    crud_user.user_crud.update(session, db_obj=user, obj_in=update_scheam)

    await email_serv.send_password_reset_email(user, background_tasks)


def user_logout(refresh_token: str, session: Session, user: User) -> None:
    """登出使用者

    並且如果傳入的 refresh token 沒有過期，則將其從資料庫中刪除。

    並且會清理資料庫中屬於該 user 的過期 token 資料

    """

    token_payload = security.get_token_payload(
        refresh_token, settings.JWT_SECRET, settings.JWT_ALGORITHM
    )

    if "error" in token_payload:

        if token_payload["error"] == "token expired":
            return None

        if token_payload["error"] == "token invalid":
            raise HTTPException(status_code=401, detail="Not authorised.")

    payload_obj = utils_schemas.jwt.JWTPayload(**token_payload)

    token_type = security.str_decode(payload_obj.p)

    if token_type != "rt":
        raise HTTPException(status_code=401, detail="Not authorised.")

    token_key = payload_obj.t

    user_token = crud_user.user_token_crud.get_by_key(session, token_key=token_key)

    if not user_token:
        raise HTTPException(status_code=401, detail="Not authorised.")

    crud_user.user_token_crud.remove(session, id=user_token.id)
    crud_user.user_token_crud.clear_up_expired_tokens(session, user_id=user.id)
