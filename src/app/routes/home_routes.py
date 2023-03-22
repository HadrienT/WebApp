from typing import Optional

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from config.templates import templates
from models.user_model import User
from dependencies import get_current_user
from models import user_model

home_router = APIRouter()


@home_router.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: Optional[user_model.User] = True):
    if current_user:
        return templates.TemplateResponse("home.html", {"request": request})
    else:
        return RedirectResponse(url="/auth/login")


@home_router.get("/me", response_model=User)
async def get_user_info(current_user: User = Depends(get_current_user)):
    return current_user
