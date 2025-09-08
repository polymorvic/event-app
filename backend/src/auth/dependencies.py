from src import secrets
from src.auth.schemas import TokenData
from src.auth.repository import get_user_by_email
from src.db.connection import db_session
from src.users.models import User

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session


secret_key = secrets.get_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def authentication(dbs: Session = Depends(db_session), token: str = Depends(oauth2_scheme)) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        assert token_data.email
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email(dbs, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
