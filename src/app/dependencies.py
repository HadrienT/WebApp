from typing import Optional

from bson import ObjectId
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
import jwt

from config.database import get_collection
from config.env import load_config
from models import user_model, token_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


async def get_user_by_id(user_id: str) -> user_model.User:
    user = get_collection('users').find_one({"_id": ObjectId(user_id)})
    return user


async def get_current_user(token: Optional[token_model.Token] = Depends(oauth2_scheme),
                           cookie_token: Optional[str] = Cookie(None)) -> user_model.User:
    config = load_config()
    used_token = token if token else cookie_token
    if not used_token:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/"},
        )

    try:
        payload = jwt.decode(used_token, config["JWT_SECRET"], algorithms=[config["JWT_ALGORITHM"]])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                headers={"Location": "/"},
            )
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")


async def check_token(token: str):
    config = load_config()
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = jwt.decode(token, config["JWT_SECRET"], algorithms=[config["JWT_ALGORITHM"]])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid access token")

        user = await get_user_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {"detail": "Valid token"}

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    