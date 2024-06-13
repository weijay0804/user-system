from pydantic import BaseModel


class UserCreateAccountResp(BaseModel):

    email: str
    name: str
    password: str
