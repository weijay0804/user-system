from pydantic import BaseModel


class UserCreateAccountResp(BaseModel):

    email: str
    name: str
    password: str


class UserVerifiyAccountReq(BaseModel):

    token: str
    email: str


class UserResetPasswordReq(BaseModel):
    new_password: str
