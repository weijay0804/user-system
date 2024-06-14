def test_create_account(client):

    data = {"email": "test@test.com", "name": "user", "password": "test"}

    response = client.post("/users", json=data)

    assert response.status_code == 201


def test_create_account_with_exist_email(client, not_active_user, test_user_data):

    data = {"email": test_user_data["email"], "name": "test_user", "password": "test"}

    response = client.post("/users", json=data)

    assert response.status_code == 409
