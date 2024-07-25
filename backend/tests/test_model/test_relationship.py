from datetime import datetime, timedelta

from app.models.user import User, UserToken


def test_user_and_usertoken_relationship(sqlite_session) -> None:

    user = User(
        email="test_user",
        name="test_user",
        password="test_user",
    )

    sqlite_session.add(user)
    sqlite_session.commit()
    sqlite_session.refresh(user)

    token = UserToken(
        user_id=user.id,
        token_key="test_token",
        expires_at=datetime.now() + timedelta(minutes=1),
        purpose="at",
    )

    sqlite_session.add(token)
    sqlite_session.commit()

    user = sqlite_session.get(User, user.id)

    user_tokens = user.tokens

    assert len(user_tokens) == 1
    assert user_tokens[0].id == token.id


def test_user_and_usertoken_one_to_many_realtionship(sqlite_session) -> None:

    user = User(
        email="test_user",
        name="test_user",
        password="test_user",
    )

    sqlite_session.add(user)
    sqlite_session.commit()
    sqlite_session.refresh(user)

    token1 = UserToken(
        user_id=user.id,
        token_key="test_token",
        expires_at=datetime.now() + timedelta(minutes=1),
        purpose="at",
    )

    token2 = UserToken(
        user_id=user.id,
        token_key="test_token2",
        expires_at=datetime.now() + timedelta(minutes=1),
        purpose="at",
    )

    sqlite_session.add_all([token1, token2])
    sqlite_session.commit()
    sqlite_session.refresh(token1)
    sqlite_session.refresh(token2)

    user = sqlite_session.get(User, user.id)

    user_tokens = user.tokens

    user_tokens_id = [t.id for t in user_tokens]

    assert len(user_tokens) == 2
    assert token1.id in user_tokens_id
    assert token2.id in user_tokens_id
