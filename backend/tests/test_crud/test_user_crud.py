from app.crud.crud_user import user_crud
from app.security import hash_string
from tests.utils import DBDataAdder


def test_user_get_by_email(sqlite_session, get_random_user_obj) -> None:

    db_adder = DBDataAdder(sqlite_session)

    user = db_adder.add_user(
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=hash_string(get_random_user_obj.raw_password),
    )

    result = user_crud.get_by_email(sqlite_session, email=get_random_user_obj.email)

    assert user.id == result.id


def test_user_get_by_email_with_not_exist_email(sqlite_session, get_random_user_obj) -> None:

    db_adder = DBDataAdder(sqlite_session)

    db_adder.add_user(
        email=get_random_user_obj.email,
        name=get_random_user_obj.name,
        password=hash_string(get_random_user_obj.raw_password),
    )

    result = user_crud.get_by_email(sqlite_session, email="not_exist_email")

    assert result is None
