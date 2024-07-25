from datetime import datetime, timedelta

import pytest
from pydantic import BaseModel
from pytest_mock import MockFixture
from sqlalchemy.exc import IntegrityError

from app.models.user import User, UserToken
from app.security import hash_string


class UserData(BaseModel):

    email: str
    name: str
    password: str


def _get_user() -> UserData:

    return UserData(email="test@test.com", name="test", password="test")


def test_create_user(sqlite_session) -> None:

    data = _get_user()

    user = User(**data.model_dump())

    sqlite_session.add(user)
    sqlite_session.commit()
    sqlite_session.refresh(user)

    assert user.id is not None
    assert user.email == data.email
    assert user.name == data.name
    assert user.is_active is False
    assert user.create_at is not None
    assert user.verified_at is None
    assert user.updated_at is None


def test_create_user_with_existing_email(sqlite_session) -> None:

    data = _get_user()

    user = User(**data.model_dump())

    sqlite_session.add(user)
    sqlite_session.commit()
    sqlite_session.refresh(user)

    new_user = User(email=data.email, name="new_user", password="new_user")

    with pytest.raises(IntegrityError):
        sqlite_session.add(new_user)
        sqlite_session.commit()


def test_generate_context_string_with_updated_at_none(sqlite_session) -> None:

    user = User()

    hashed_pwd = hash_string("test")

    user.password = hashed_pwd
    user.create_at = datetime(2024, 1, 1, 12, 0, 0)

    context_string = user.get_context_string("TEST_CONTEXT")

    assert context_string == f"TEST_CONTEXT{hashed_pwd[-6:]}20240101120000"


def test_generate_context_string_with_updated_at_set(sqlite_session) -> None:

    user = User()

    hashed_pwd = hash_string("test")

    user.password = hashed_pwd
    user.create_at = datetime(2024, 1, 1, 23, 0, 0)
    user.updated_at = datetime(2024, 1, 1, 12, 0, 0)

    context_string = user.get_context_string("TEST_CONTEXT")

    assert context_string == f"TEST_CONTEXT{hashed_pwd[-6:]}20240101120000"


def test_create_usertoken_with_valid_data(sqlite_session, mocker: MockFixture) -> None:

    user_id = 1

    token = UserToken(
        user_id=user_id,
        token_key="valid_key",
        expires_at=datetime.now() + timedelta(minutes=1),
        purpose="at",
    )

    sqlite_session.add(token)
    sqlite_session.commit()
    sqlite_session.refresh(token)

    fetched_token = sqlite_session.query(UserToken).filter_by(user_id=user_id).first()

    assert fetched_token is not None
    assert fetched_token.user_id == user_id
    assert fetched_token.token_key == "valid_key"
    assert fetched_token.purpose == "at"
