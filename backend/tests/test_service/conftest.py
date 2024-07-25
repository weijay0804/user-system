import pytest

from tests.utils import RandomUser, random_user_gen


@pytest.fixture(scope="function")
def get_random_user_obj() -> RandomUser:

    return random_user_gen.gen_random_user()
