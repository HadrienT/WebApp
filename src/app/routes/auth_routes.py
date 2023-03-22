from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from models import token_model
from controllers.auth_controller import login_route, login_page_display
from dependencies import check_token, oauth2_scheme

auth_router = APIRouter()


@auth_router.get("/login")
def login_page(request: Request) -> HTMLResponse:
    return login_page_display(request)


@auth_router.post("/token", response_model=token_model.Token)
@auth_router.post("/login", response_model=token_model.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> token_model.Token:
    return await login_route(form_data)


@auth_router.get("/token")
async def check_token_route(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    return await check_token(token)
