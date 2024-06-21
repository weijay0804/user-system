from datetime import datetime
from typing import Dict

import pytest

from app.models.user import User
from app.security import hash_password


@pytest.fixture(scope="function")
def test_user_data() -> Dict[str, str]:

    return {"email": "test@test.com", "name": "user1", "password": "test"}


@pytest.fixture(scope="function")
def not_active_user(test_session, test_user_data) -> User:

    model = User()
    model.email = test_user_data["email"]
    model.name = test_user_data["name"]
    model.password = hash_password(test_user_data["password"])

    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)

    return model


@pytest.fixture(scope="function")
def user(test_session, test_user_data) -> User:

    model = User()
    model.email = test_user_data["email"]
    model.name = test_user_data["name"]
    model.password = hash_password(test_user_data["password"])
    model.is_active = True
    model.verified_at = datetime.now()

    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)

    return model
