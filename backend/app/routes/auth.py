from fastapi import APIRouter, BackgroundTasks, Depends, Header, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_session
from app.models.user import User
from app.schemas import request_schemas, response_schemas
from app.services import auth_serv

auth_router = APIRouter(prefix="/auth", tags=["Auth"], responses={404: {"message": "Not found."}})


@auth_router.post("/verifiy", status_code=status.HTTP_200_OK)
async def verify_user_account(
    data: request_schemas.user.UserVerifiyAccountReq,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """使用傳入的 token 和 email 驗證使用者帳戶，並發送帳戶已啟用 email 至使用者信箱"""

    await auth_serv.activate_user_account(data, session, background_tasks)

    return JSONResponse({"message": "Account has been verified."})


@auth_router.post("/verifiy/resend", status_code=status.HTTP_200_OK)
async def resend_verifiy_email(
    data: request_schemas.auth.ReSendVerifiyEmailReq,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """重新寄送用戶認證 email 至使用者信箱"""

    await auth_serv.resend_verifiy_email(data, background_tasks, session)

    return JSONResponse({"message": "Verification email has been sent."})


@auth_router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=response_schemas.auth.JWTokenResp
)
def user_login(
    data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
):
    """使用者登入，並回傳 JWT"""

    return auth_serv.get_login_token(data, session)


@auth_router.post("/token/refresh", response_model=response_schemas.auth.JWTokenResp)
def refresh_token(refresh_token=Header(), session: Session = Depends(get_session)):
    """使用 refresh token 取得新的 access token"""

    return auth_serv.refresh_token(refresh_token, session)


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password_request(
    data: request_schemas.user.UserForgotPasswordReq,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """用戶忘記密碼，重新設定請求，會發送重新設定密碼的 email 至使用者信箱"""

    await auth_serv.forgot_password(data, session, background_tasks)

    return JSONResponse(content={"message": "A reset password email has been sent."})


@auth_router.put("/forgot-password/reset", status_code=status.HTTP_200_OK)
async def forgot_password_reset(
    data: request_schemas.user.UserForgotPasswordResetReq,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """根據傳入的 token 和 email，重設使用者密碼，並寄送密碼已經重新設定的 email 至使用者信箱"""

    await auth_serv.forgot_password_reset(data, background_tasks, session)

    return JSONResponse(content={"message": "Password has been reset."})


@auth_router.get("/logout")
def user_logout(
    refresh_token=Header(),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """登出使用者"""

    auth_serv.user_logout(refresh_token, session, user)

    return JSONResponse(content={"message": "You have been logged out."})
