from fastapi import FastAPI
from src.users.routes import users_router

app = FastAPI()

app.include_router(users_router, prefix="/users")


@app.get("/")
async def root():
    return {"message": "Hello"}
