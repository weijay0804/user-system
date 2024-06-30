from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.config.settings import get_settings
from app.crud import crud_user
from app.models.user import User
from app.schemas import utils_schemas
from app.security import get_token_payload, str_decode

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_session() -> Generator[Session, None, None]:
    """取得 db session 實例"""

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()


def get_token_user(token: str, session: Session) -> User:
    """從 token 中取得使用者資訊"""

    payload = get_token_payload(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    user = None

    # NOTE 這邊可以再重構一下
    if "error" in payload:
        if payload["error"] == "token expired":
            raise HTTPException(status_code=401, detail="Token expired.")

        if payload["error"] == "token invalid":
            raise HTTPException(status_code=401, detail="Not authorised.")

    try:
        payload_obj = utils_schemas.jwt.JWTPayload(**payload)

    except ValueError:
        raise HTTPException(status_code=401, detail="Not authorised.")

    # 防止傳入的 token 不是 access_token 而是 refresh_token 而造成錯誤
    token_purpose = str_decode(payload_obj.p)

    if token_purpose != "at":
        raise HTTPException(status_code=401, detail="Not authorised.")

    user_id = str_decode(payload_obj.sub)

    user = crud_user.user_crud.get(session, id=user_id)

    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    """從 token 中取得使用者資訊，並檢查 token 是否有效"""

    user = get_token_user(token, session)

    if not user:
        raise HTTPException(status_code=401, detail="Not authorised.")

    return user
