import base64
import logging
import secrets
from datetime import datetime, timedelta
from typing import Dict

import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)


def generate_token(payload: dict, secret: dict, algo: dict, expiry: timedelta) -> str:
    """產生 JWT token"""

    expiry = datetime.now() + expiry

    payload.update({"exp": expiry})

    return jwt.encode(payload, secret, algorithm=algo)


def get_unique_string(byte: int = 8) -> str:
    """取得特定位數的唯一值字串"""

    return secrets.token_urlsafe(byte)


def str_encode(string: str) -> str:
    """將字串進行 base85 編碼"""

    return base64.b85encode(string.encode("ascii")).decode("ascii")


def str_decode(string: str) -> str:

    return base64.b85decode(string.encode("ascii")).decode("ascii")


def get_token_payload(token: str, secret: str, alog: str) -> Dict[str, str]:

    try:
        payload = jwt.decode(token, secret, alog)

    except Exception as jwt_exec:
        logging.debug(f"JWT Error: {str(jwt_exec)}")
        payload = None

    return payload
