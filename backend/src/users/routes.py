from fastapi import APIRouter, Depends
from src.users.models import User
from src.users.schemas import UserIn, UserOut
from src.db.connection import db_session
from sqlalchemy.orm import Session
from src.users.repository import user_create


users_router = APIRouter()


@users_router.post("/register", response_model=UserOut)
async def create_user(user_in: UserIn, dbs: Session = Depends(db_session)) -> User:
    return user_create(user_in, dbs)
