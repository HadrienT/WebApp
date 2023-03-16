import os
from datetime import datetime, timedelta
from typing import Any, Union

import jwt
import dotenv
from bson.objectid import ObjectId
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config.database import get_collection


dotenv.load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION = timedelta(minutes=int(os.getenv("JWT_EXPIRATION")))


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict[str, str]) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + JWT_EXPIRATION})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Union[dict[str, Any], None]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def get_user_by_username(username: str) -> Union[Any, None]:
    user = get_collection('users').find_one({"username": username})
    return user


def get_user_by_id(user_id: str) -> Union[Any, None]:
    user = get_collection('users').find_one({"_id": ObjectId(user_id)})
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def login(username: str, password: str) -> dict[str, str]:
    user = get_user_by_username(username)
    if user is None or not verify_password(password, user["hashed_password"]):
        return None
    access_token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}


async def login_route(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    username = form_data.username
    password = form_data.password
    token = await login(username, password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
