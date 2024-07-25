from fastapi import APIRouter, BackgroundTasks, Depends, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_session, oauth2_scheme
from app.models.user import User
from app.schemas import request_schemas, response_schemas
from app.services import user_serv

user_router = APIRouter(prefix="/users", tags=["Users"], responses={404: {"message": "Not found."}})
user_auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"message": "Not found."}},
    dependencies=[Depends(oauth2_scheme)],
)


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def register_user(
    data: request_schemas.user.UserCreateAccountReq,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """註冊使用者"""

    await user_serv.create_user_account(data, session, backgroundtasks=background_tasks)

    return JSONResponse({"message": "Account has been created."}, status_code=201)


@user_router.put("/password")
async def reset_password(
    data: request_schemas.user.UserResetPasswordReq,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """重新設定用戶密碼，並發送密碼已經重新設定的 email 至使用者信箱"""

    await user_serv.reset_password(data, user, session, background_tasks)

    return JSONResponse({"message": "Password has been reset."})


@user_auth_router.get("/me", response_model=response_schemas.user.FetchUserResp)
def fetch_user(user: User = Depends(get_current_user)):

    return user
