from fastapi import APIRouter

users_router = APIRouter()


@users_router.get("/")
async def root():
    return {"message": "Hello"}
