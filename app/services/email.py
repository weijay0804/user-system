from fastapi import BackgroundTasks
from fastapi_mail import MessageSchema, MessageType

from app.config.email import fm
from app.config.settings import get_settings
from app.models.user import User
from app.security import hash_password

settings = get_settings()


async def send_email(
    recipients: list,
    subject: str,
    context: str,
    template_name: str,
    background_tasks: BackgroundTasks,
) -> None:

    message = MessageSchema(
        subject=subject, recipients=recipients, template_body=context, subtype=MessageType.html
    )

    background_tasks.add_task(fm.send_message, message, template_name=template_name)


async def send_account_verification_email(user: User, background_tasks: BackgroundTasks) -> None:
    """在背景寄送用帳號認證信件"""

    context_string = user.get_context_string(context=settings.USER_VERIFY_ACCOUNT_EMAIL_CONTEXT)

    token = hash_password(context_string)

    active_url = f"{settings.FRONTEND_HOST}/auth/account-verify?token={token}&email={user.email}"

    data = {"app_name": settings.APP_NAME, "name": user.name, "activate_url": active_url}

    subject = f"Account Verifiaction - {settings.APP_NAME}"

    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="users/account-verification.html",
        context=data,
        background_tasks=background_tasks,
    )
