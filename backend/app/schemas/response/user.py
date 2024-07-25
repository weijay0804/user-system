from pydantic import BaseModel


class FetchUserResp(BaseModel):
    """取得使用者資料回應體"""

    id: int
    email: str
    name: str
