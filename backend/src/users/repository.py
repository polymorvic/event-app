import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from src.users.models import User
from src.users.schemas import UserIn
from src.auth.helpers import get_password_hash



def user_create(user_in: UserIn, dbs: Session) -> User:
    db_user = dbs.execute(
        select(User).where(User.email == user_in.email)
    ).scalar_one_or_none()
    if db_user:
        raise HTTPException(
            status_code=400, detail="User with given email already exists"
        )
    hashed_password = get_password_hash(user_in.password)
    user_data = user_in.model_dump()
    user_data["password"] = hashed_password
    user = User(**user_data)
    dbs.add(user)
    dbs.commit()
    return user
