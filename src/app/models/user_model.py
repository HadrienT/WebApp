from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    username: str
    hashed_password: str
    password: Optional[str] = None
    balance: Optional[float] = 100.0
    is_active: Optional[bool] = True
    creation_date: Optional[str] = None
    storage_limit: Optional[int] = 10 * 1024 * 1024

    class Config:
        arbitrary_types_allowed = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
