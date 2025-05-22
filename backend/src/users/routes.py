from fastapi import APIRouter

users_router = APIRouter()


@users_router.post("/")
async def root():
    return {"message": "Hello"}
