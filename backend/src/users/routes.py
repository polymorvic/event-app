from fastapi import APIRouter, Depends, HTTPException
from src.users.models import User
from src.users.schemas import UserIn, UserOut
from src.db.connection import db_session
from sqlalchemy.orm import  Session
from sqlalchemy import select



users_router = APIRouter()


@users_router.post("/register", response_model=UserOut)
async def create_user(user_in: UserIn, dbs: Session = Depends(db_session)) -> User:
    # db_user = dbs.query(User).filter(User.email == user_in.email).first() - stary syntax
    db_user = dbs.execute(select(User).where(User.email == user_in.email)).scalar_one_or_none() # all()
    if db_user:
        raise HTTPException(status_code=400, detail="User with given email already exists")
    user_data = user_in.model_dump()
    user = User(**user_data)
    dbs.add(user)
    dbs.commit()
    return user
