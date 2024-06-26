from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.config.settings import get_settings
from app.crud import user_token_crud
from app.models.user import User
from app.security import get_token_payload, str_decode

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_session() -> Generator[Session, None, None]:

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()


def get_token_user(token: str, session: Session) -> User:

    payload = get_token_payload(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    user = None

    if payload:

        # 防止傳入的 token 不是 access_token 而是 refresh_token 而造成錯誤
        try:
            token_type = str_decode(payload["ty"])

        except KeyError:
            pass

        if token_type != "at":
            raise HTTPException(status_code=401, detail="Not authorised.")

        user_token_id = str_decode(payload["r"])
        user_id = str_decode(payload["sub"])
        access_key = payload["a"]

        user = user_token_crud.get_user(
            session, token_id=user_token_id, access_key=access_key, user_id=user_id
        )

    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:

    user = get_token_user(token, session)

    if not user:
        raise HTTPException(status_code=401, detail="Not authorised.")

    return user
