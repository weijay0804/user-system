from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.routes import base_router, guest_router, user_router


def create_app():

    settings = get_settings()

    app = FastAPI()
    app.include_router(user_router)
    app.include_router(base_router)
    app.include_router(guest_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()
