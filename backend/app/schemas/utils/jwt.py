from datetime import datetime

from pydantic import BaseModel


class JWTPayload(BaseModel):
    """JWT 資訊

    其中 `sub` 和 `p` 使用 `str_encode` 來編碼

    """

    sub: str
    t: str
    p: str
    exp: datetime
