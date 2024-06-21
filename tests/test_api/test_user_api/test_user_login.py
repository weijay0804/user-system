def test_user_login(client, user, test_user_data):

    data = {"username": user.email, "password": test_user_data["password"]}

    response = client.post("/auth/login", data=data)

    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None
    assert response.json()["expires_at"] is not None


def test_user_login_with_not_active_user(client, not_active_user, test_user_data):

    data = {"username": not_active_user.email, "password": test_user_data["password"]}

    response = client.post("/auth/login", data=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Your account is not active."


def test_user_login_with_invalid_email(client, user, test_user_data):

    data = {"username": "invalid@test.com", "password": test_user_data["password"]}

    response = client.post("/auth/login", data=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password."


def test_user_login_with_wrong_password(client, user, test_user_data):

    data = {"username": user.email, "password": "wrong_password"}

    response = client.post("/auth/login", data=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password."


def test_user_login_with_not_verify(client, not_active_user, test_session, test_user_data):

    not_active_user.is_active = True

    test_session.add(not_active_user)
    test_session.commit()
    test_session.refresh(not_active_user)

    data = {"username": not_active_user.email, "password": test_user_data["password"]}

    response = client.post("/auth/login", data=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Your account is not verified."
