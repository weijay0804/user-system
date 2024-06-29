from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserDBCreate(BaseModel):
    """建立使用者資料"""

    email: str
    name: str
    password: str


class UserDBUpdate(BaseModel):
    """更新使用者資料"""

    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    verified_at: Optional[datetime] = None
    update_at: Optional[datetime] = None


class UserTokenDBCreate(BaseModel):
    """建立使用者 token 資料"""

    user_id: int
    access_key: str
    refresh_key: str
    expires_at: datetime


class UserTokenDBUpdate(BaseModel):
    """更新使用者 token 資料"""

    access_key: Optional[str] = None
    refresh_key: Optional[str] = None
    expires_at: Optional[str] = None
