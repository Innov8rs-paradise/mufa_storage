from src.database import get_db

def test_get_db_returns_generator():
    db_gen = get_db()
    db = next(db_gen)
    assert db is not None
    db.close()