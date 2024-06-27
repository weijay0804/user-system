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


class UserForgotPasswordReq(BaseModel):
    email: str


class UserForgotPasswordResetReq(BaseModel):
    token: str
    email: str
    new_password: str
