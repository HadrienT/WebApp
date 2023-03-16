from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    username: str
    hashed_password: str
    password: Optional[str] = None
    balance: Optional[float] = 0.0

    class Config:
        arbitrary_types_allowed = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
