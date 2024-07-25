import pytest
from fastapi import BackgroundTasks
from fastapi_mail import MessageSchema, MessageType
from pytest_mock import MockFixture

from app.config.email import fm
from app.services import email_serv


@pytest.mark.asyncio
async def test_send_email(mocker: MockFixture) -> None:

    mock_background_tasks = BackgroundTasks()

    recipients = ["test@test.com"]
    subject = "test"
    context = "test"
    template_name = "test"

    mock_send_message = mocker.patch.object(fm, "send_message", return_value=None)

    await email_serv.send_email(
        recipients=recipients,
        subject=subject,
        context=context,
        template_name=template_name,
        background_tasks=mock_background_tasks,
    )

    assert len(mock_background_tasks.tasks) == 1
    task = mock_background_tasks.tasks[0]
    assert task.func == mock_send_message
    assert task.args == (
        MessageSchema(
            subject=subject, recipients=recipients, template_body=context, subtype=MessageType.html
        ),
    )
    assert task.kwargs == {"template_name": template_name}
