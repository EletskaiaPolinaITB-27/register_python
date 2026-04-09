from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    TokenResponseSchema,
    TokenRefreshSchema,
    UserResponseSchema,
)
from src.database import get_db


SECRET_KEY = "secret"
ALGORITHM = "HS256"

ACCESS_EXPIRE = 15  # минут
REFRESH_EXPIRE = 7  # дней

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer()

user_router = APIRouter(prefix="/users", tags=["Users"])


# =========================
# HELPERS
# =========================
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_access_token(user: User):
    payload = {
        "user_id": user.id,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user: User):
    payload = {
        "user_id": user.id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=REFRESH_EXPIRE),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Wrong token type")

    user = db.query(User).filter(User.id == payload["user_id"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# =========================
# ROUTES
# =========================
@user_router.post("/register", response_model=TokenResponseSchema)
def register(data: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.login == data.login).first():
        raise HTTPException(400, "Login already exists")

    user = User(
        login=data.login,
        email=data.email,
        hashed_password=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }


@user_router.post("/login", response_model=TokenResponseSchema)
def login(data: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == data.login).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Wrong login or password")

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }


@user_router.post("/refresh")
def refresh(data: TokenRefreshSchema, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(401, "Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(401, "Wrong token type")

    user = db.query(User).filter(User.id == payload["user_id"]).first()

    if not user:
        raise HTTPException(401, "User not found")

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }


@user_router.get("/me", response_model=UserResponseSchema)
def me(user: User = Depends(get_current_user)):
    return user