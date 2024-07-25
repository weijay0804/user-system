import os
from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail

from app.config.settings import get_settings

settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", ""),
    MAIL_PORT=os.environ.get("MAIL_PORT", 1025),
    MAIL_SERVER=os.environ.get("MAIL_SERVER", "localhost"),
    MAIL_STARTTLS=os.environ.get("MAIL_STARTTLS", False),
    MAIL_SSL_TLS=os.environ.get("MAIL_SSL_TLS", False),
    MAIL_DEBUG=True,
    MAIL_FROM=os.environ.get("MAIL_FROM", "noreply@test.com"),
    MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME", settings.APP_NAME),
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
    USE_CREDENTIALS=os.environ.get("USE_CREDENTIALS", False),
)

fm = FastMail(conf)
