from datetime import datetime
from typing import Union
from bson import ObjectId
from fastapi import Request, HTTPException
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

from config.templates import templates
from config.database import get_collection
from models import user_model
from controllers.auth_controller import create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def create_user(user: user_model.UserCreate) -> user_model.User:
    user_collection = get_collection('users')
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        return None

    hashed_password = get_password_hash(user.password)
    new_user = user_model.User(email=user.email,
                               username=user.username,
                               hashed_password=hashed_password,
                               is_active=True,
                               creation_date=datetime.utcnow().isoformat())
    user_dict = new_user.dict()
    user_dict["_id"] = ObjectId(user_dict["id"]) if user_dict.get("id") else ObjectId()
    del user_dict["id"]

    result = user_collection.insert_one(user_dict)
    new_user.id = str(result.inserted_id)
    return new_user


def user_to_token_data(user: user_model.User) -> dict:
    return {"sub": user.id}


async def register_user(user: user_model.User) -> Union[JSONResponse, HTTPException]:
    registered_user = await create_user(user)
    if registered_user:

        # Convert the User object to a dictionary with the necessary data
        token_data = user_to_token_data(registered_user)

        # Create a token for the user
        token = create_access_token(token_data)
        # Return a JSON response with the token and redirect URL
        return JSONResponse(content={"access_token": token.access_token, "redirectUrl": "/home"})
    else:
        raise HTTPException(status_code=400, detail="Email address is already in use.")


async def reset_balance(current_user: user_model.User) -> JSONResponse:
    result = get_collection("users").update_one({"_id": current_user["_id"]}, {"$set": {"balance": 100}})
    return JSONResponse(content={"modified_count": result.modified_count})


async def get_balance(current_user: user_model.User) -> JSONResponse:
    return JSONResponse(content={"balance": current_user["balance"]})


async def deduct_balance(current_user: user_model.User, amount: int) -> JSONResponse:
    if current_user["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    result = get_collection("users").update_one({"_id": current_user["_id"]}, {"$inc": {"balance": -amount}})
    return JSONResponse(content={"modified_count": result.modified_count})


async def get_user_memory_usage(current_user: user_model.User) -> JSONResponse:
    images = get_collection("images").find({"user_id": str(current_user["_id"])})
    memory_usage = 0
    for image in images:
        memory_usage += image["file_size"]

    return {"memory_usage": memory_usage, "max_memory_allowed": current_user["storage_limit"]}
