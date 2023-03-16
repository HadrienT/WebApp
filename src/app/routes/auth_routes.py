from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.token import Token
from controllers.auth_controller import login_route


auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_route(form_data)
