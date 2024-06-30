import base64
import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict

import jwt
from jwt.exceptions import ExpiredSignatureError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_string(string: str) -> str:
    """將字串進行 hash"""

    return pwd_context.hash(string)


def verify_hashed_string(plain_string: str, hashed_string: str) -> bool:
    """比對 hash 字串是否正確"""

    return pwd_context.verify(plain_string, hashed_string)


def generate_token(payload: dict, secret: dict, algo: dict) -> str:
    """產生 JWT token"""

    return jwt.encode(payload, secret, algorithm=algo)


def get_unique_string(byte: int = 8) -> str:
    """取得特定位數的唯一值字串"""

    return secrets.token_urlsafe(byte)


def str_encode(string: str) -> str:
    """將字串進行 base85 編碼"""

    return base64.b85encode(string.encode("ascii")).decode("ascii")


def str_decode(string: str) -> str:
    """將 base85 編碼的字串進行解碼"""

    return base64.b85decode(string.encode("ascii")).decode("ascii")


def get_token_payload(token: str, secret: str, alog: str) -> Dict[str, str]:
    """取得 token 資訊

    如果 token 有效，回傳 token 資訊，否則回傳錯誤訊息

    錯誤訊息格式如下

    - token 過期：
    ```
    {
        "error": "token expired"
    }
    ```

    - token 無效:
    ```
    {
        "error": "token invalid"
    }
    ```
    """

    try:
        payload = jwt.decode(token, secret, alog)

    except ExpiredSignatureError:
        payload = {"error": "token expired"}

    except Exception as jwt_exec:
        logging.debug(f"JWT Error: {str(jwt_exec)}")
        payload = {"error": "token invalid"}

    return payload
