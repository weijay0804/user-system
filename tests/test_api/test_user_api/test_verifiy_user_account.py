from app.config.settings import get_settings
from app.crud import user_crud
from app.security import hash_password

settings = get_settings()


def test_verifiy_user_account(client, not_active_user, test_session):

    token_context = not_active_user.get_context_string(settings.USER_VERIFY_ACCOUNT_EMAIL_CONTEXT)
    token = hash_password(token_context)

    data = {"email": not_active_user.email, "token": token}

    response = client.post("/users/verifiy", json=data)

    assert response.status_code == 200

    activated_user = user_crud.get_by_email(test_session, email=not_active_user.email)

    assert activated_user.updated_at is not None
    assert activated_user.verified_at is not None
    assert activated_user.is_active is True


def test_verifiy_link_doesnot_work_twicr(client, not_active_user):

    token_context = not_active_user.get_context_string(settings.USER_VERIFY_ACCOUNT_EMAIL_CONTEXT)
    token = hash_password(token_context)

    data = {"email": not_active_user.email, "token": token}

    response = client.post("/users/verifiy", json=data)

    assert response.status_code == 200

    response = client.post("/users/verifiy", json=data)

    assert response.status_code == 400


def test_verifiy_link_with_invalid_token(client, not_active_user, test_session):

    data = {"email": not_active_user.email, "token": "invalid token"}

    response = client.post("/users/verifiy", json=data)

    assert response.status_code == 400

    inactivated_user = user_crud.get_by_email(test_session, email=not_active_user.email)

    assert inactivated_user.is_active is False
    assert inactivated_user.verified_at is None


def test_verifiy_link_with_invalid_email(client, not_active_user, test_session):

    token_context = not_active_user.get_context_string(settings.USER_VERIFY_ACCOUNT_EMAIL_CONTEXT)
    token = hash_password(token_context)

    data = {"email": "invalid@test.com", "token": token}

    response = client.post("/users/verifiy", json=data)

    assert response.status_code == 400

    inactivated_user = user_crud.get_by_email(test_session, email=not_active_user.email)

    assert inactivated_user.is_active is False
    assert inactivated_user.verified_at is None
