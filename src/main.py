from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import Base, engine, get_db
import src.crud, src.schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=src.schemas.UserOut)
def create_user(user: src.schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = src.crud.get_user(db, user.id)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return src.crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=src.schemas.UserOut)
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = src.crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user