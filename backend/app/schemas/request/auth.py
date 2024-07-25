from pydantic import BaseModel


class ReSendVerifiyEmailReq(BaseModel):
    email: str
