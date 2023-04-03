from fastapi import APIRouter, File, Query, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse

from config.templates import jinja_templates
from dependencies import get_current_user
from models import user_model, image_model, infer_model
from controllers import home_controller

home_router = APIRouter()


@home_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return jinja_templates.TemplateResponse("home.html", {"request": request})


@home_router.get("/me", response_model=user_model.User)
async def get_user_info(current_user: user_model.User = Depends(get_current_user)):
    return current_user


@home_router.get("/images", response_model=list[image_model.ImageResponse])
async def get_images_route(current_user: user_model.User = Depends(get_current_user)):
    return await home_controller.get_images(current_user)


@home_router.post("/images/upload")
async def upload_image_route(file: UploadFile = File(...), current_user: user_model.User = Depends(get_current_user)):
    return await home_controller.upload_image(file=file, current_user=current_user)


@home_router.get('/inference', response_class=HTMLResponse)
async def inference(request: Request):
    return jinja_templates.TemplateResponse("inference.html", {"request": request})


@home_router.get("/myaccount", response_class=HTMLResponse)
async def my_account(request: Request, current_user: user_model.User = Depends(get_current_user)):
    return await home_controller.show_account(request, current_user)


@home_router.post("/inference")
async def api_apply_algorithm(request_data: infer_model.InferRequest):
    return await home_controller.process_image_data(request_data.image_data, request_data.image_id)


@home_router.delete("/images/delete/{image_id}")
async def delete_image_route(image_id: str, current_user: user_model.User = Depends(get_current_user)):
    return await home_controller.delete_image(image_id, current_user)


@home_router.get("/upgrade", response_class=HTMLResponse)
async def upgrade(request: Request, current_user: user_model.User = Depends(get_current_user)):
    return await home_controller.show_upgrade(request, current_user)


@home_router.get("/aboutUs", response_class=HTMLResponse)
async def about_us(request: Request):
    return jinja_templates.TemplateResponse("aboutUs.html", {"request": request})


@home_router.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request, planId: str = Query(None)):
    return jinja_templates.TemplateResponse("checkout.html", {"request": request, "planId": planId})
