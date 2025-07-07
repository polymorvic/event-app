from fastapi import Depends, HTTPException, status
from fastapi import APIRouter
from src.auth.schemas import Token, Oauth2EmailRequestForm
from datetime import timedelta
from src.auth.helpers import authenticate_user, create_access_token
from sqlalchemy.orm import Session
from src.db.connection import db_session


auth_router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 90


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Oauth2EmailRequestForm, dbs: Session = Depends(db_session)
) -> Token:
    user = authenticate_user(dbs, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_activated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not activated, please check your email",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
