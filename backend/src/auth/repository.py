from src.users.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select


def get_user_by_email(dbs: Session, email: str) -> User | None:
    return dbs.execute(select(User).where(User.email == email)).scalar_one_or_none()
