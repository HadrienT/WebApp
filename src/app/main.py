from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from routes import user_routes, auth_routes, home_routes
from config.database import startup_event, shutdown_event

from fastapi import Depends
from models.user_model import User
from dependencies import get_current_user


app = FastAPI()
app.on_event("startup")(startup_event)
app.on_event("shutdown")(shutdown_event)

app.include_router(user_routes.user_router, prefix="/user", tags=["User"])
app.include_router(auth_routes.auth_router, prefix="/auth", tags=["Auth"])
app.include_router(home_routes.home_router, prefix="/home", tags=["Home"])

# Configure CORS to allow requests from the front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/app/static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/home", status_code=303)


# Example of a protected route
@app.get("/protected", response_model=User)
async def protected_route(current_user: User = Depends(get_current_user)):
    return current_user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('app.main:app', host="localhost", port=8001, reload=True)
