from fastapi import APIRouter, Depends
from src.auth.dependencies import authentication
from src.users.models import User
from src.users.schemas import UserIn, UserOut
from src.db.connection import db_session
from sqlalchemy.orm import Session
from src.users.repository import user_create
from src.mail.service import send_mail


users_router = APIRouter()


@users_router.post("/register", response_model=UserOut)
async def create_user(user_in: UserIn, dbs: Session = Depends(db_session)) -> User:
    user = user_create(user_in, dbs)
    await send_mail(user.email)
    return user


@users_router.get("/me", response_model=UserOut)
async def current_user(current_user: User = Depends(authentication)) -> User:
    return current_user
