from app.crud import user_crud


def test_get_by_email(sqlite_session, test_create_user_obj):

    user = user_crud.create(sqlite_session, obj_in=test_create_user_obj)

    user_by_email = user_crud.get_by_email(sqlite_session, email=user.email)

    assert user_by_email.id == user.id
    assert user_by_email.name == user.name
