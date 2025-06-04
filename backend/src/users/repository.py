from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from src.users.models import User
from src.users.schemas import UserIn


def user_create(user_in: UserIn, dbs: Session) -> User:
    db_user = dbs.execute(
        select(User).where(User.email == user_in.email)
    ).scalar_one_or_none()
    if db_user:
        raise HTTPException(
            status_code=400, detail="User with given email already exists"
        )
    user_data = user_in.model_dump()
    user = User(**user_data)
    dbs.add(user)
    dbs.commit()
    return user
