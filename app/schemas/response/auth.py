from datetime import datetime

from pydantic import BaseModel


class JWToken(BaseModel):
    """JWT 資訊回應體"""

    token: str
    expires_at: datetime


class JWTokenResp(BaseModel):
    """JWT 資訊回應體"""

    access_token: JWToken
    refresh_token: JWToken
