from fastapi import BackgroundTasks
from fastapi_mail import MessageSchema, MessageType

from app import security
from app.config.email import fm
from app.config.settings import get_settings
from app.models.user import User

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

    token = security.hash_string(context_string)

    active_url = f"{settings.FRONTEND_HOST}{settings.FRONTEND_ACTIVE_ACCOUNT_URL}?token={token}&email={user.email}"

    data = {"app_name": settings.APP_NAME, "name": user.name, "activate_url": active_url}

    subject = f"Account Verifiaction - {settings.APP_NAME}"

    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="users/account-verification.html",
        context=data,
        background_tasks=background_tasks,
    )


async def send_account_verifiaction_confirmation_email(
    user: User, background_tasks: BackgroundTasks
) -> None:
    """在背景寄送帳戶認證成功提醒 email"""

    data = {
        "app_name": settings.APP_NAME,
        "name": user.name,
    }

    subject = f"帳戶啟用成功 - {settings.APP_NAME}"

    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="users/account-verification-confirmation.html",
        context=data,
        background_tasks=background_tasks,
    )


async def send_password_reset_email(user: User, background_tasks: BackgroundTasks) -> None:

    data = {"app_name": settings.APP_NAME, "name": user.name}

    subject = f"Password Reseted - {settings.APP_NAME}"

    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="users/password-reset.html",
        context=data,
        background_tasks=background_tasks,
    )


async def send_forgot_password_reset_email(user: User, background_tasks: BackgroundTasks) -> None:

    string_context = user.get_context_string(context=settings.USER_FORGOT_PASSWORD_EMAIL_CONTEXT)
    token = security.hash_string(string_context)

    reset_url = f"{settings.FRONTEND_HOST}{settings.FRONTEND_FORGOT_PASSWORD_RESET_URL}?token={token}&email={user.email}"

    data = {"app_name": settings.APP_NAME, "name": user.name, "reset_url": reset_url}

    subject = f"Password Reset - {settings.APP_NAME}"

    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="users/forgot-password-reset.html",
        context=data,
        background_tasks=background_tasks,
    )
