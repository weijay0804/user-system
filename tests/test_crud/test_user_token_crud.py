import time
from datetime import datetime, timedelta

from app.crud import user_crud, user_token_crud
from app.schemas import db_schemas


def test_get_user(sqlite_session, test_create_user_obj):

    user = user_crud.create(sqlite_session, obj_in=test_create_user_obj)

    token_obj = db_schemas.UserTokenDBCreate(
        user_id=user.id,
        access_key="access_key",
        refresh_key="refresh_key",
        expires_at=datetime.now() + timedelta(minutes=1),
    )

    user_token = user_token_crud.create(sqlite_session, obj_in=token_obj)

    token_user = user_token_crud.get_user(
        sqlite_session, token_id=user_token.id, access_key=user_token.access_key, user_id=user.id
    )

    assert token_user is not None


def test_get_user_with_invalid_access_key(sqlite_session, test_create_user_obj):

    user = user_crud.create(sqlite_session, obj_in=test_create_user_obj)

    token_obj = db_schemas.UserTokenDBCreate(
        user_id=user.id,
        access_key="access_key",
        refresh_key="refresh_key",
        expires_at=datetime.now() + timedelta(minutes=1),
    )

    user_token = user_token_crud.create(sqlite_session, obj_in=token_obj)

    token_user = user_token_crud.get_user(
        sqlite_session, token_id=user_token.id, access_key="invalid access key", user_id=user.id
    )

    assert token_user is None


def test_get_user_with_expires_time(sqlite_session, test_create_user_obj):

    user = user_crud.create(sqlite_session, obj_in=test_create_user_obj)

    token_obj = db_schemas.UserTokenDBCreate(
        user_id=user.id,
        access_key="access_key",
        refresh_key="refresh_key",
        expires_at=datetime.now() + timedelta(seconds=1),
    )

    user_token = user_token_crud.create(sqlite_session, obj_in=token_obj)

    time.sleep(1)

    token_user = user_token_crud.get_user(
        sqlite_session, token_id=user_token.id, access_key=user_token.access_key, user_id=user.id
    )

    assert token_user is None
