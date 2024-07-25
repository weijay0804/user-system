from datetime import datetime, timedelta, timezone

import pytest
from fastapi import BackgroundTasks, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas import request_schemas, response_schemas, utils_schemas
from app.services import auth_serv, email_serv


@pytest.mark.asyncio
async def test_activate_user_account_success(mocker: MockerFixture) -> None:

    mock_session = mocker.Mock(spec=Session)
    mock_backgroundtasks = mocker.Mock(spec=BackgroundTasks)
    mock_user = mocker.Mock(spec=User)

    mock_user.email = "example@example.com"
    mock_user.get_context_string.return_value = "hashed_token"

    mocker.patch("app.crud.crud_user.user_crud.get_by_email", return_value=mock_user)
    mocker.patch("app.security.verify_hashed_string", return_value=True)
    mocker.patch(
        "app.services.email_serv.send_account_verifiaction_confirmation_email", return_value=None
    )

    data = request_schemas.user.UserVerifiyAccountReq(
        email="example@example.com", token="hashed_token"
    )
    await auth_serv.activate_user_account(data, mock_session, mock_backgroundtasks)

    assert mock_user.is_active is True
    assert mock_user.verified_at is not None
    mock_session.add.assert_called_once_with(mock_user)
    mock_session.commit.assert_called_once()
    email_serv.send_account_verifiaction_confirmation_email.assert_called_once_with(
        mock_user, mock_backgroundtasks
    )


@pytest.mark.asyncio
async def test_activate_user_with_not_exist_user(mocker: MockerFixture) -> None:

    mock_session = mocker.Mock(spec=Session)
    mock_backgroundtasks = mocker.Mock(spec=BackgroundTasks)

    mocker.patch("app.crud.crud_user.user_crud.get_by_email", return_value=None)

    data = request_schemas.user.UserVerifiyAccountReq(
        email="example@example.com", token="hashed_token"
    )
    with pytest.raises(HTTPException) as e:
        await auth_serv.activate_user_account(data, mock_session, mock_backgroundtasks)

    assert e.value.status_code == 400
    assert e.value.detail == "This link is not valid."


@pytest.mark.asyncio
async def test_activate_user_with_invalid_token(mocker: MockerFixture) -> None:

    mock_session = mocker.Mock(spec=Session)
    mock_backgroundtasks = mocker.Mock(spec=BackgroundTasks)
    mock_user = mocker.Mock(spec=User)

    mock_user.email = "example@example.com"
    mock_user.get_context_string.return_value = "hashed_token"

    mocker.patch("app.crud.crud_user.user_crud.get_by_email", return_value=mock_user)
    mocker.patch("app.security.verify_hashed_string", return_value=False)

    data = request_schemas.user.UserVerifiyAccountReq(
        email="example@example.com", token="hashed_token"
    )
    with pytest.raises(HTTPException) as e:
        await auth_serv.activate_user_account(data, mock_session, mock_backgroundtasks)

    assert e.value.status_code == 400
    assert e.value.detail == "This link is not valid."


@pytest.mark.asyncio
async def test_activate_user_account_exception_handling(mocker: MockerFixture):

    session = mocker.Mock(spec=Session)
    backgroundtasks = mocker.Mock(spec=BackgroundTasks)

    mock_user = mocker.Mock(spec=User)
    mock_user.is_active = False
    mock_user.get_context_string.return_value = "mocked_context_string"

    mocker.patch("app.crud.crud_user.user_crud.get_by_email", return_value=mock_user)

    data = request_schemas.user.UserVerifiyAccountReq(
        email="test@example.com", token="invalid_token"
    )

    mocker.patch('app.security.verify_hashed_string', side_effect=Exception("mocked exception"))

    log_exception = mocker.patch('logging.exception')

    with pytest.raises(HTTPException) as exc_info:
        await auth_serv.activate_user_account(data, session, backgroundtasks)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "This link is not valid."

    log_exception.assert_called_once()
    args, _ = log_exception.call_args
    assert "mocked exception" in str(args[0])

    assert mock_user.is_active is False


def test_generate_payload_for_access_token(get_random_user_obj, mocker: MockerFixture) -> None:

    mocker.patch('app.services.auth_serv.settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 15)
    mocker.patch('app.security.get_unique_string', return_value='unique_string')
    mocker.patch('app.security.str_encode', side_effect=lambda x: x)

    user = User(
        id=1,
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=get_random_user_obj.raw_password,
    )

    payload = auth_serv._generate_token_payload(user, "at")

    assert payload.sub == "1"
    assert payload.t == "unique_string"
    assert payload.p == "at"
    assert payload.exp.timestamp() - datetime.now(timezone.utc).timestamp() == pytest.approx(
        15 * 60, rel=1e-2
    )


def test_generate_payload_for_refresh_token(get_random_user_obj, mocker: MockerFixture) -> None:

    mocker.patch('app.services.auth_serv.settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES', 30)
    mocker.patch('app.security.get_unique_string', return_value='unique_string')
    mocker.patch('app.security.str_encode', side_effect=lambda x: x)

    user = User(
        id=1,
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=get_random_user_obj.raw_password,
    )

    payload = auth_serv._generate_token_payload(user, "rt")

    assert payload.sub == "1"
    assert payload.t == "unique_string"
    assert payload.p == "rt"
    assert payload.exp.timestamp() - datetime.now(timezone.utc).timestamp() == pytest.approx(
        30 * 60, rel=1e-2
    )


def test_generate_payload_with_invalid_purpose(get_random_user_obj) -> None:

    user = User(
        id=1,
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=get_random_user_obj.raw_password,
    )

    with pytest.raises(ValueError) as e:
        auth_serv._generate_token_payload(user, "invalid_purpose")

    assert e.value.args[0] == "Invalid token purpose."


def test_generate_jwt_token(mocker: MockerFixture) -> None:

    mocker.patch('app.services.auth_serv.settings.JWT_SECRET', 'testsecret')
    mocker.patch('app.services.auth_serv.settings.JWT_ALGORITHM', 'HS256')

    exp = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    payload = utils_schemas.jwt.JWTPayload(sub="testuser", t="token_key", p="at", exp=exp)

    token_response = auth_serv._generate_token(payload)

    assert isinstance(token_response, response_schemas.auth.JWToken)
    assert token_response.expires_at == exp


def test_get_login_token(mocker: MockerFixture, get_random_user_obj) -> None:

    session = mocker.Mock(spec=Session)
    user = User(
        id=1,
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=get_random_user_obj.raw_password,
        is_active=True,
        verified_at=datetime.now(tz=timezone.utc),
    )

    mocker.patch("app.crud.crud_user.user_crud.get_by_email", return_value=user)
    mocker.patch("app.security.verify_hashed_string", return_value=True)
    mocker.patch(
        "app.services.auth_serv._generate_token_payload",
        return_value=utils_schemas.jwt.JWTPayload(sub="1", t="token", p="at", exp=datetime.now()),
    )
    mocker.patch(
        "app.services.auth_serv._generate_token",
        return_value=response_schemas.auth.JWToken(token="token", expires_at=datetime.now()),
    )
    mocker.patch("app.crud.crud_user.user_token_crud.create")

    data = OAuth2PasswordRequestForm(
        username=get_random_user_obj.email, password=get_random_user_obj.raw_password
    )

    response = auth_serv.get_login_token(data=data, session=session)

    assert response.access_token.token == "token"
    assert response.refresh_token.token == "token"
