from pydantic import BaseModel

class UserCreate(BaseModel):
    id: str
    email: str
    name: str
    picture: str | None = None

class UserOut(BaseModel):
    id: str
    email: str
    name: str
    picture: str | None = None

    class Config:
        orm_mode = True