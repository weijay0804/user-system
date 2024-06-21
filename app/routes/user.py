from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_session, oauth2_scheme
from app.models.user import User
from app.schemas import request_schemas, response_schemas
from app.services import user as user_services

user_router = APIRouter(prefix="/users", tags=["Users"], responses={404: {"message": "Not found."}})
guest_router = APIRouter(prefix="/auth", tags=["Auth"], responses={404: {"message": "Not found."}})
auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"message": "Not found."}},
)


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def register_user(
    data: request_schemas.UserCreateAccountResp,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """註冊使用者"""

    await user_services.create_user_account(data, session, backgroundtasks=background_tasks)

    return JSONResponse({"message": "Account has been created."}, status_code=201)


@user_router.post("/verifiy", status_code=status.HTTP_200_OK)
async def verify_user_account(
    data: request_schemas.UserVerifiyAccountReq,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """認證使用者"""

    await user_services.activate_user_account(data, session, background_tasks)

    return JSONResponse({"message": "Account has been verified."})


@guest_router.post("/login", response_model=response_schemas.JWTokenResp)
def user_login(
    data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
):

    return user_services.get_login_token(data, session)


@auth_router.get("/me", response_model=response_schemas.FetchUserResp)
def fetch_user(user: User = Depends(get_current_user)):

    return user
