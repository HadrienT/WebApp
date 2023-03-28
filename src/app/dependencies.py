from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from config.database import get_collection
from config.env import load_config
from models import user_model, token_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


async def get_user_by_id(user_id: str) -> user_model.User:
    user = get_collection('users').find_one({"_id": ObjectId(user_id)})
    return user


async def get_current_user(token: token_model.Token = Depends(oauth2_scheme)) -> user_model.User:
    config = load_config()
    try:
        payload = jwt.decode(token, config["JWT_SECRET"], algorithms=[config["JWT_ALGORITHM"]])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.PyJWTError:
        print("JWT Error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def check_token(token: str = Depends(oauth2_scheme)):
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
