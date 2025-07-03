import pytest
from pydantic import ValidationError
from src.schemas import UserCreate, UserOut

def test_user_create_valid():
    user = UserCreate(
        id="user_1",
        email="test@example.com",
        name="Test User",
        picture="http://example.com/pic.jpg"
    )
    assert user.id == "user_1"
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.picture == "http://example.com/pic.jpg"

def test_user_create_without_picture():
    user = UserCreate(
        id="user_2",
        email="test2@example.com",
        name="No Pic User"
    )
    assert user.picture is None

def test_user_create_missing_field():
    with pytest.raises(ValidationError):
        UserCreate(
            email="missing@example.com",
            name="Missing ID"
        )

def test_user_out_valid():
    user = UserOut(
        id="user_3",
        email="out@example.com",
        name="Output User",
        picture=None
    )
    assert user.id == "user_3"
    assert user.email == "out@example.com"
    assert user.name == "Output User"
    assert user.picture is None