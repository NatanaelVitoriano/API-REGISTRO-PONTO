from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.auth import authenticate_user, get_current_user
from auth.jwt import create_access_token
from db import get_db
from schemas import User, UserCreate, User, Token, User
from crud import get_user_by_user_name, create_user, create_time_log

router = APIRouter()

@router.post("/users/", tags=["Users"], response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_user_name(db, user_name=user.user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="User name already registered")
    return create_user(db=db, user=user)

@router.post("/users/login", tags=["Users"], response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/current", tags=["Users"], response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user