from fastapi import FastAPI

from app.routes import base_router, user_router


def create_app():

    app = FastAPI()
    app.include_router(user_router)
    app.include_router(base_router)

    return app


app = create_app()
