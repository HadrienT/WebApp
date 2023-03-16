from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from config.templates import templates

# from controllers.home_controller import 


home_router = APIRouter()


@home_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
