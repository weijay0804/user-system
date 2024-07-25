from app.services.user import _generate_token


def test_fetch_user(client, user, test_session):

    data = _generate_token(user, test_session)

    header = {"Authorization": f"Bearer {data.access_token}"}

    response = client.get("/users/me", headers=header)

    assert response.status_code == 200
    assert response.json().get("password") is None


def test_fetch_user_with_refresh_token(client, user, test_session):

    data = _generate_token(user, test_session)

    header = {"Authorization": f"Bearer {data.refresh_token}"}

    response = client.get("/users/me", headers=header)

    assert response.status_code == 401


def test_fetch_user_with_invalid_token(client, user, test_session):

    data = _generate_token(user, test_session)

    header = {"Authorization": f"Bearer {data.access_token[:-2]}_wd"}

    response = client.get("/users/me", headers=header)

    assert response.status_code == 401
