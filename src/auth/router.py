from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig, TokenPayload
from src.database import get_db
from src.auth.models import User
from src.auth.schemas import UserRegisterSchema


config = AuthXConfig(
    JWT_SECRET_KEY="test-secret-key",
    JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(config=config)
security = HTTPBearer()

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)





@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserRegisterSchema,    
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует"
        )

    new_user = User(
        email=user_data.email,
        password=user_data.password,   
        first_name="",          
        last_name=""
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)              

    access_token = auth.create_access_token(uid=new_user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Регистрация прошла успешно"
    }





@user_router.post("/login")
def login(
    email: str,          
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user or user.password != password:
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль"
        )

    access_token = auth.create_access_token(uid=user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }






@user_router.get("/protected")
def protected(payload: TokenPayload = Depends(auth.access_token_required),
              credentials = Depends(security)):
    return {"message": payload.sub}