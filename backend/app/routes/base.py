from fastapi import APIRouter
from fastapi.responses import JSONResponse

base_router = APIRouter(tags=["Base"], responses={404: {"message": "Not found."}})


@base_router.get("/")
def index():

    return JSONResponse({"message": "welcome to user system."})
