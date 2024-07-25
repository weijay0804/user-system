from typing import Optional

from pydantic import BaseModel
from pytest_mock import MockFixture
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from app.config.database import Base
from app.crud.base import CRUDBase


class MockModel(Base):
    __tablename__ = "mock_model"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=True)


def test_get(mocker: MockFixture) -> None:

    db = mocker.Mock(spec=Session)

    crud = CRUDBase(MockModel)

    valid_id = 1
    expected_record = MockModel(id=valid_id)

    db.get.return_value = expected_record

    result = crud.get(db, valid_id)

    db.get.assert_called_once_with(MockModel, valid_id)
    assert result == expected_record


def test_get_multi(mocker: MockFixture) -> None:

    db = mocker.Mock(spec=Session)
    query = mocker.Mock()
    db.query.return_value = query

    model = mocker.Mock()
    query.offset.return_value.limit.return_value.all.return_value = [model, model]

    crud = CRUDBase(model=model)

    result = crud.get_multi(db)

    assert len(result) == 2
    assert result == [model, model]


def test_create(mocker: MockFixture) -> None:

    class MockCreateScheam(BaseModel):
        id: int

    db_session = mocker.Mock(spec=Session)
    crud = CRUDBase(MockModel)

    mock_obj_in = MockCreateScheam(id=1)

    db_session.add = mocker.Mock()
    db_session.commit = mocker.Mock()
    db_session.refresh = mocker.Mock()

    result = crud.create(db=db_session, obj_in=mock_obj_in)

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(result)

    assert result.id == 1


def test_update(mocker: MockFixture) -> None:

    class MockUpdateScheam(BaseModel):
        id: Optional[int] = None
        username: Optional[str] = None

    db = mocker.Mock(spec=Session)

    crud = CRUDBase(MockModel)

    db_obj = MockModel(id=1, username="test")
    obj_in = MockUpdateScheam(username="test_update")

    updated_obj = crud.update(db, db_obj=db_obj, obj_in=obj_in)

    assert updated_obj.username == "test_update"
    db.add.assert_called_once_with(db_obj)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_obj)


def test_update_with_dict(mocker: MockFixture) -> None:

    db = mocker.Mock(spec=Session)

    crud = CRUDBase(MockModel)

    db_obj = MockModel(id=1, username="test")
    obj_in = {"username": "test_update"}

    updated_obj = crud.update(db, db_obj=db_obj, obj_in=obj_in)

    assert updated_obj.username == "test_update"
    db.add.assert_called_once_with(db_obj)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_obj)


def test_remove(mocker: MockFixture) -> None:

    db = mocker.Mock(spec=Session)
    model = mocker.Mock()
    crud = CRUDBase(model)

    obj = mocker.Mock()

    db.get.return_value = obj

    crud.remove(db, id=1)

    db.get.assert_called_once_with(model, 1)
    db.delete.assert_called_once_with(obj)
    db.commit.assert_called_once()
