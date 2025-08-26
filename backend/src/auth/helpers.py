from src.auth.repository import get_user_by_email
from sqlalchemy.orm import Session
from src.users.models import User
import bcrypt
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
import jwt
from itsdangerous import URLSafeSerializer, BadSignature
from src import secrets

ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    return hashed_password.decode("utf-8")


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


def email_verification_serializer() -> URLSafeSerializer:
    return URLSafeSerializer(secrets.get_secret_key())


def generate_verification_token(user_id: int, user_email: str) -> URLSafeSerializer:
    serializer = email_verification_serializer()
    return serializer.dumps(f"{user_id}:{user_email}")


def verify_email_token(token: str, dbs: Session) -> User | None:
    serializer = email_verification_serializer()
    try:
        data = serializer.loads(token)
        print(f"/n/n/n/n/{data} /n/n/n/n")
        user_id, user_email = data.split(":")
        user = dbs.execute(
            select(User).where(User.id == int(user_id), User.email == user_email)
        ).scalar_one_or_none()
        return user
    except BadSignature:
        return None
