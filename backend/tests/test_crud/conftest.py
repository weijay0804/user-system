from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config.database import Base
from app.config.settings import get_settings
from tests.utils import RandomUser, random_user_gen

settings = get_settings()


@pytest.fixture(scope="function", name="sqlite_session")
def sqlite_session() -> Generator[Session, None, None]:
    """取得 sqlite orm session，並會初始化和刪除資料表"""

    engine = create_engine(settings.TEST_DB_URI, poolclass=StaticPool)
    SessionTest = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
    )

    Base.metadata.create_all(bind=engine)
    session = SessionTest()

    try:
        yield session

    finally:

        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def get_random_user_obj() -> RandomUser:

    return random_user_gen.gen_random_user()