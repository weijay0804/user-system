from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.deps import get_session
from app.schemas import request_schemas
from app.services import user as user_services

user_router = APIRouter(prefix="/users", tags=["Users"], responses={404: {"message": "Not found."}})


@user_router.post("", status_code=status.HTTP_201_CREATED)
def register_user(
    data: request_schemas.UserCreateAccountResp, session: Session = Depends(get_session)
):
    """註冊使用者"""

    user_services.create_user_account(data, session)

    return JSONResponse({"message": "Account has been created."}, status_code=201)


@user_router.post("/verify", status_code=status.HTTP_200_OK)
def verify_user_account(data):
    """認證使用者"""
    pass
