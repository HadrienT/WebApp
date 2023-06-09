from datetime import datetime
from typing import Any, Union

import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from config.database import get_collection
from config.templates import jinja_templates
from config.env import load_config
from models import token_model, user_model
from dependencies import get_current_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict[str, str]) -> token_model.Token:
    config = load_config()
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + config["JWT_EXPIRATION"]})
    encoded_jwt = jwt.encode(to_encode, config["JWT_SECRET"], algorithm=config["JWT_ALGORITHM"])
    token = token_model.Token(access_token=encoded_jwt, token_type="bearer")
    return token


async def get_user_by_username(username: str) -> Union[Any, None]:
    user = await get_collection('users').find_one({"username": username})
    return user


def get_user_by_mail(email: str) -> Union[Any, None]:
    user = get_collection('users').find_one({"email": email})
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def login_user(email: str, password: str) -> token_model.Token:
    user = get_user_by_mail(email)
    if user is None or not verify_password(password, user["hashed_password"]):
        print("User not found")
        return None
    print("User found")
    access_token = create_access_token({"sub": str(user["_id"])})
    return access_token


async def login_route(form_data: OAuth2PasswordRequestForm = Depends()) -> token_model.Token:
    email = form_data.username
    password = form_data.password
    token = await login_user(email, password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


def login_page_display(request: Request, current_user: user_model.User = Depends(get_current_user)) -> HTMLResponse:
    return jinja_templates.TemplateResponse("signin.html", {"request": request})
