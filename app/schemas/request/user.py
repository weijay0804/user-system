from pydantic import BaseModel


class UserCreateAccountReq(BaseModel):
    """建立使用者帳戶請求體"""

    email: str
    name: str
    password: str


class UserVerifiyAccountReq(BaseModel):
    """認證使用者帳戶請求體"""

    token: str
    email: str


class UserResetPasswordReq(BaseModel):
    """重新設定使用者密碼請求體，這個是針對以經登入的使用者重新設定密碼"""

    new_password: str


class UserForgotPasswordReq(BaseModel):
    """使用者忘記密碼請求體"""

    email: str


class UserForgotPasswordResetReq(BaseModel):
    """使用者忘記密碼，重新設定密碼請求體，這是針對以經忘記密碼的使用者重新設定密碼"""

    token: str
    email: str
    new_password: str
