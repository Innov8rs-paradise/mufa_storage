from src.models import User
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base

import pytest

# Use in-memory SQLite database for model testing
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

def test_user_model_creation(session: Session):
    user = User(id="user123", email="user@example.com", name="Example User")
    session.add(user)
    session.commit()

    fetched = session.query(User).filter_by(id="user123").first()
    assert fetched is not None
    assert fetched.email == "user@example.com"
    assert fetched.name == "Example User"