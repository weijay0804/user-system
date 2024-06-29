from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.routes import auth, base, user


def create_app():

    settings = get_settings()

    app = FastAPI()
    app.include_router(user.user_auth_router)
    app.include_router(user.user_router)
    app.include_router(base.base_router)
    app.include_router(auth.auth_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()
