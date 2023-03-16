from fastapi import APIRouter, Body, Request
from fastapi.responses import HTMLResponse, JSONResponse

from models import user_model
from controllers import user_controller


user_router = APIRouter()


@user_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request) -> HTMLResponse:
    return await user_controller.register(request)


# create a new user
@user_router.post("/register", response_class=HTMLResponse)
async def new_user(user_request: user_model.UserCreate = Body(...)) -> JSONResponse:
    return await user_controller.register_user(user_request)
