from pydantic import BaseModel


class FetchUserResp(BaseModel):

    id: int
    email: str
    name: str
