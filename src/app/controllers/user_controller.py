from bson import ObjectId
from fastapi import Request, Response, HTTPException
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

from config.templates import templates
from config.database import get_collection
from models.user_model import User, UserCreate
from controllers.auth_controller import create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def create_user(user: UserCreate) -> User:
    user_collection = get_collection('users')
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        return None

    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, username=user.username, hashed_password=hashed_password)
    user_dict = new_user.dict()
    user_dict["_id"] = ObjectId(user_dict["id"]) if user_dict.get("id") else ObjectId()
    del user_dict["id"]

    result = user_collection.insert_one(user_dict)
    new_user.id = str(result.inserted_id)
    return new_user


def user_to_token_data(user: User) -> dict:
    return {"sub": user.id}


async def register_user(user: User) -> Response:
    registered_user = await create_user(user)
    if registered_user:

        # Convert the User object to a dictionary with the necessary data
        token_data = user_to_token_data(registered_user)

        # Create a token for the user
        token = create_access_token(token_data)

        # Create a response object with the token set in the 'Authorization' header
        response = JSONResponse(content={"message": "Account created successfully"})
        response.headers["Authorization"] = f"Bearer {token}"
        return response
    else:
        raise HTTPException(status_code=400, detail="Error creating account.")
