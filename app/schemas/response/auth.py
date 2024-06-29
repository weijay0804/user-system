from datetime import datetime

from pydantic import BaseModel


class JWTokenResp(BaseModel):
    """JWT 資訊回應體"""

    access_token: str
    refresh_token: str
    expires_at: datetime
