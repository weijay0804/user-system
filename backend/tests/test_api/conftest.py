from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config.database import Base
from app.config.email import fm
from app.config.settings import get_settings
from app.deps import get_session
from app.main import create_app

settings = get_settings()

engine = create_engine(
    settings.TEST_DB_URI, poolclass=StaticPool, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

testing_app = create_app()


@pytest.fixture(scope="function")
def test_session() -> Generator[Session, None, None]:

    session = SessionTesting()

    try:
        yield session

    finally:
        session.close()


@pytest.fixture(scope="function")
def test_app() -> Generator[FastAPI, None, None]:

    Base.metadata.create_all(bind=engine)

    yield testing_app

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_app, test_session) -> TestClient:

    def _test_db() -> Generator[Session, None, None]:

        try:
            yield test_session

        finally:
            pass

    test_app.dependency_overrides[get_session] = _test_db
    fm.config.SUPPRESS_SEND = 1

    return TestClient(app=test_app)
