from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from routes import user_routes, auth_routes, home_routes
from config.database import startup_event, shutdown_event
from config.templates import jinja_templates
from middlewares import cors_middleware

app = FastAPI()
app.on_event("startup")(startup_event)
app.on_event("shutdown")(shutdown_event)

app.include_router(user_routes.user_router, prefix="/user", tags=["User"])
app.include_router(auth_routes.auth_router, prefix="/auth", tags=["Auth"])
app.include_router(home_routes.home_router, prefix="/home", tags=["Home"])

cors_middleware.setup_cors(app)

app.mount("/static", StaticFiles(directory="src/app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return jinja_templates.TemplateResponse("index.html", {"request": request})
