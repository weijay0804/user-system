from datetime import datetime, timedelta, timezone

from app.crud.crud_user import user_token_crud
from app.models.user import UserToken
from app.security import hash_string
from tests.utils import DBDataAdder


def test_user_token_get_by_key(sqlite_session, get_random_user_obj) -> None:

    db_adder = DBDataAdder(sqlite_session)

    user = db_adder.add_user(
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=hash_string(get_random_user_obj.raw_password),
    )

    token = db_adder.add_user_token(
        user_id=user.id,
        token_key="valid_token_key",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=1),
    )

    result = user_token_crud.get_by_key(sqlite_session, token_key="valid_token_key")

    assert result.id == token.id


def test_user_token_get_by_key_with_expired_token(sqlite_session, get_random_user_obj) -> None:

    db_adder = DBDataAdder(sqlite_session)

    user = db_adder.add_user(
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=hash_string(get_random_user_obj.raw_password),
    )

    token = db_adder.add_user_token(
        user_id=user.id,
        token_key="expired_token_key",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )

    result = user_token_crud.get_by_key(sqlite_session, token_key="expired_token_key")

    assert result.id == token.id


def test_user_token_clear_up_expired_tokens(sqlite_session, get_random_user_obj) -> None:

    db_adder = DBDataAdder(sqlite_session)

    user = db_adder.add_user(
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=hash_string(get_random_user_obj.raw_password),
    )

    token = db_adder.add_user_token(
        user_id=user.id,
        token_key="expired_token_key",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )

    user_token_crud.clear_up_expired_tokens(sqlite_session, user_id=user.id)

    result = sqlite_session.get(UserToken, token.id)

    assert result is None


def test_user_token_clear_up_expired_tokens_with_multiple_users(
    sqlite_session, get_random_user_obj
) -> None:

    db_adder = DBDataAdder(sqlite_session)

    user = db_adder.add_user(
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=hash_string(get_random_user_obj.raw_password),
    )

    user2 = db_adder.add_user(
        email="2" + get_random_user_obj.email,
        name="2" + get_random_user_obj.name,
        password=hash_string(get_random_user_obj.raw_password),
    )

    token = db_adder.add_user_token(
        user_id=user.id,
        token_key="expired_token_key",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )

    token2 = db_adder.add_user_token(
        user_id=user2.id,
        token_key="expired_token_key",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )

    user_token_crud.clear_up_expired_tokens(sqlite_session, user_id=user.id)

    result = sqlite_session.get(UserToken, token.id)
    result2 = sqlite_session.get(UserToken, token2.id)

    assert result is None
    assert result2 is not None
