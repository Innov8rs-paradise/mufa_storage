from src import crud, schemas
from src.models import User

def test_create_user(db_session):
    user = schemas.UserCreate(id="test_id", email="test@example.com", name="Test User")
    db_user = crud.create_user(db_session, user)
    assert db_user.id == "test_id"
    assert db_user.email == "test@example.com"

def test_get_user(db_session):
    user = schemas.UserCreate(id="u123", email="u123@example.com", name="U123")
    crud.create_user(db_session, user)
    result = crud.get_user(db_session, "u123")
    assert result is not None
    assert result.name == "U123"

def test_get_user_not_found(db_session):
    result = crud.get_user(db_session, "nonexistent")
    assert result is None