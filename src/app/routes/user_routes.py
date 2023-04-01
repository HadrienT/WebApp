from fastapi import APIRouter, Body, Query, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse

from models import user_model
from controllers import user_controller
from dependencies import get_current_user


user_router = APIRouter()


@user_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request) -> HTMLResponse:
    return await user_controller.register(request)


# create a new user
@user_router.post("/register", response_class=JSONResponse)
async def new_user(user_request: user_model.UserCreate = Body(...)) -> JSONResponse:
    return await user_controller.register_user(user_request)


@user_router.post("/reset_balance")
async def reset_balance_route(current_user: user_model.User = Depends(get_current_user)):
    return await user_controller.reset_balance(current_user)


@user_router.get("/get_balance", response_class=HTMLResponse)
async def get_balance_route(current_user: user_model.User = Depends(get_current_user)):
    return await user_controller.get_balance(current_user)


@user_router.put("/deduct_balance")
async def deduct_balance_route(amount: float = Query(..., gt=0), current_user: user_model.User = Depends(get_current_user)):
    return await user_controller.deduct_balance(current_user, amount)


@user_router.get("/memory_usage")
async def memory_usage_route(current_user: user_model.User = Depends(get_current_user)):
    return await user_controller.get_user_memory_usage(current_user)
