from fastapi import FastAPI

from app.routes import user_router


def create_app():

    app = FastAPI()
    app.include_router(user_router)

    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "ok"}
