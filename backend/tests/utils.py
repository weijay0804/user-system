import random
import string
from datetime import datetime

from pydantic import BaseModel

from app.models.user import User, UserToken


class RandomUser(BaseModel):
    name: str
    email: str
    raw_password: str


class RandomUserGen:

    def __gen_random_string(self, length: int) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def __gen_random_username(self) -> str:
        first_name_length = random.randint(3, 7)
        last_name_length = random.randint(5, 10)

        first_name = self.__gen_random_string(first_name_length)
        last_name = self.__gen_random_string(last_name_length)

        return first_name + last_name

    def __gen_random_email_(self, domain="test@test.com") -> str:
        name_length = random.randint(5, 10)
        name = self.__gen_random_string(name_length)

        return f"{name}@{domain}"

    def __gen_random_password_(self, length: int = 10) -> str:
        all_chars = string.ascii_letters + string.digits + string.punctuation

        password = ''.join(random.choices(all_chars, k=length))
        return password

    def gen_random_user(self) -> RandomUser:
        username = self.__gen_random_username()
        email = self.__gen_random_email_()
        raw_password = self.__gen_random_password_()

        return RandomUser(name=username, email=email, raw_password=raw_password)


class DBDataAdder:

    def __init__(self, session) -> None:
        self.session = session

    def add_user(self, email: str, name: str, password: str) -> User:

        user = User(email=email, name=name, password=password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def add_user_token(
        self, user_id: int, token_key: str, expires_at: datetime, purpose: str = "at"
    ) -> UserToken:

        user_token = UserToken(
            user_id=user_id,
            token_key=token_key,
            expires_at=expires_at,
            purpose=purpose,
        )

        self.session.add(user_token)
        self.session.commit()
        self.session.refresh(user_token)

        return user_token


random_user_gen = RandomUserGen()
