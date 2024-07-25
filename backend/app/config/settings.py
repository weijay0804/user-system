import os
from functools import lru_cache
from pathlib import Path
from typing import List
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    # APP
    APP_NAME: str = os.environ.get("APP_NAME", "User System")
    APP_ENV: str = os.environ.get("APP_ENV", "dev")

    # CORS
    ALLOW_ORIGINS: str = os.environ.get("ALLOW_ORIGINS", "")
    ALLOW_ORIGINS_LIST: List[str] = ALLOW_ORIGINS.strip().replace(" ", "").split(",")

    # Frontend
    FRONTEND_HOST: str = os.environ.get("FRONTEND_HOST", "http://127.0.0.1:5500")
    FRONTEND_ACTIVE_ACCOUNT_URL: str = os.environ.get(
        "FRONTEND_ACTIVE_ACCOUNT_URL", "/auth/account-verifiy"
    )
    FRONTEND_FORGOT_PASSWORD_RESET_URL: str = os.environ.get(
        "FRONTEND_FORGOT_PASSWORD_RESET_URL", "/forgot-password-reset"
    )

    # MySQL
    MYSQL_HOST: str = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER: str = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.environ.get("MYSQL_PASSWORD", "root")
    MYSQL_PORT: int = os.environ.get("MYSQL_PORT", 3306)
    MYSQL_DB: str = os.environ.get("MYSQL_DB", "user_system")

    DATABASE_URI: str = (
        f"mysql+pymysql://{MYSQL_USER}:%s@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        % quote_plus(MYSQL_PASSWORD)
    )

    # Testing config
    TEST_DB_URI: str = "sqlite://"

    # Email config
    # Email Context
    USER_VERIFY_ACCOUNT_EMAIL_CONTEXT: str = os.environ.get(
        "USER_VERIFY_ACCOUNT_EMAIL_CONTEXT", "verify-account"
    )
    USER_FORGOT_PASSWORD_EMAIL_CONTEXT: str = os.environ.get(
        "USER_FORGOT_PASSWORD_EMAIL_CONTEXT", "password-reset"
    )

    # JWT config
    JWT_SECRET: str = os.environ.get(
        "JWT_SECRET", "ae0359c0c2eb9ced85498375ef480cbd5b0eb30f0579c17443866b72f762b873"
    )
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 3))
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 15)
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
