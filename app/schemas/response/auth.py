from datetime import datetime

from pydantic import BaseModel


class JWTokenResp(BaseModel):

    access_token: str
    refresh_token: str
    expires_at: datetime
