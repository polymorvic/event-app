from fastapi import FastAPI

from src.auth.routes import auth_router
from src.users.routes import users_router

app = FastAPI()

app.include_router(users_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")
