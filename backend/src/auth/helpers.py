from src.auth.repository import get_user_by_email
from passlib.context import CryptContext
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.users.models import User
from datetime import datetime, timedelta, timezone
import jwt
from src import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(dbs: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(dbs, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secrets.get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt