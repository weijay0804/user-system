from app.crud import user_crud
from app.schemas import db_schemas


def test_get(sqlite_session, test_create_user_obj):

    user = user_crud.get(sqlite_session, 1)

    assert user is None

    db_user = user_crud.create(sqlite_session, obj_in=test_create_user_obj)

    user = user_crud.get(sqlite_session, db_user.id)

    assert user is not None
    assert user.email == test_create_user_obj.email


def test_get_multi(sqlite_session, test_create_user_obj):

    user1 = user_crud.create(sqlite_session, obj_in=test_create_user_obj)

    user2_obj = db_schemas.UserDBCreate(email="test2@test.com", name="test", password="test")

    user2 = user_crud.create(sqlite_session, obj_in=user2_obj)

    users = user_crud.get_multi(sqlite_session, limit=1)

    assert len(users) == 1

    users = user_crud.get_multi(sqlite_session)

    assert len(users) == 2
    assert user1 in users
    assert user2 in users


def test_create(sqlite_session, test_create_user_obj):

    user = user_crud.create(sqlite_session, obj_in=test_create_user_obj)

    assert user.id is not None
    assert user.email == test_create_user_obj.email
    assert user.name == test_create_user_obj.name


def test_update(sqlite_session, test_create_user_obj):

    user = user_crud.create(sqlite_session, obj_in=test_create_user_obj)

    assert user.email == test_create_user_obj.email
    assert user.updated_at is None

    user_update_in = db_schemas.UserDBUpdate(email="update@test.com")

    updated_user = user_crud.update(sqlite_session, db_obj=user, obj_in=user_update_in)

    assert updated_user.id == user.id
    assert updated_user.name == user.name
    assert updated_user.email == "update@test.com"
    assert updated_user.updated_at is not None


def test_remove(sqlite_session, test_create_user_obj):

    user = user_crud.create(sqlite_session, obj_in=test_create_user_obj)

    user_db = user_crud.get(sqlite_session, user.id)

    assert user_db is not None

    user_crud.remove(sqlite_session, id=user_db.id)

    removed_user = user_crud.get(sqlite_session, user_db.id)

    assert removed_user is None
