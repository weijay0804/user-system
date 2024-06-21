from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserDBCreate(BaseModel):

    email: str
    name: str
    password: str


class UserDBUpdate(BaseModel):

    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    verified_at: Optional[datetime] = None
    update_at: Optional[datetime] = None


class UserTokenDBCreate(BaseModel):

    user_id: int
    access_key: str
    refresh_key: str
    expires_at: datetime


class UserTokenDBUpdate(BaseModel):

    access_key: Optional[str] = None
    refresh_key: Optional[str] = None
    expires_at: Optional[str] = None
