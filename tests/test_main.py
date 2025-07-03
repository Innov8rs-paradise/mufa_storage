import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.schemas import UserCreate, UserOut
import src.crud

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "id": "user_123",
        "email": "test@example.com",
        "name": "Test User",
        "picture": "http://example.com/pic.jpg"
    }

def test_create_user_success(monkeypatch, test_user):
    # Mock get_user to return None (user does not exist)
    monkeypatch.setattr(src.crud, "get_user", lambda db, user_id: None)
    # Mock create_user to return the user data
    monkeypatch.setattr(src.crud, "create_user", lambda db, user: UserOut(**test_user))

    response = client.post("/users/", json=test_user)
    assert response.status_code == 200
    assert response.json() == test_user

def test_create_user_already_exists(monkeypatch, test_user):
    # Mock get_user to return a user (already exists)
    monkeypatch.setattr(src.crud, "get_user", lambda db, user_id: UserOut(**test_user))

    response = client.post("/users/", json=test_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_read_user_success(monkeypatch, test_user):
    # Mock get_user to return a user
    monkeypatch.setattr(src.crud, "get_user", lambda db, user_id: UserOut(**test_user))

    response = client.get(f"/users/{test_user['id']}")
    assert response.status_code == 200
    assert response.json() == test_user

def test_read_user_not_found(monkeypatch):
    # Mock get_user to return None
    monkeypatch.setattr(src.crud, "get_user", lambda db, user_id: None)

    response = client.get("/users/nonexistent_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"