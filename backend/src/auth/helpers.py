from src.auth.repository import get_user_by_email
from sqlalchemy.orm import Session
from src.users.models import User
import bcrypt
from datetime import datetime, timedelta, timezone
import jwt
from src import secrets

ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    return hashed_password.decode('utf-8')


def authenticate_user(dbs: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(dbs, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(
    data: dict[str, str | datetime], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secrets.get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt
