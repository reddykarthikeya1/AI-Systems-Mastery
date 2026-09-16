#!/usr/bin/env python3
"""Multi-Tenant RBAC Authentication Microservice.

Module 14 (Authentication, Authorization & Security) Turnkey Project Implementation.
Demonstrates Bcrypt salted hashing, PyJWT bearer token issuance, and RBAC dependencies.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

# ==========================================
# 1. Configuration & Security Constants
# ==========================================

JWT_SECRET = "production-secure-32-byte-hex-secret-token-key"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI(
    title="Multi-Tenant RBAC Authentication Microservice",
    version="1.0.0",
)


# ==========================================
# 2. Pydantic Models & Storage
# ==========================================

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    role: str = Field("viewer", pattern="^(admin|editor|viewer)$")


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInDB(UserResponse):
    hashed_password: str


users_db: dict[str, UserInDB] = {}
user_id_counter = 0


# ==========================================
# 3. Security Helpers
# ==========================================

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_jwt(user: UserInDB) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# ==========================================
# 4. Dependency Injection & RBAC Guard
# ==========================================

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("username")
        if not username or username not in users_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return users_db[username]
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature") from exc


def require_role(allowed_roles: list[str]):
    def role_checker(current_user: Annotated[UserInDB, Depends(get_current_user)]) -> UserInDB:
        if current_user.role not in allowed_roles and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires roles: {allowed_roles} (User has: {current_user.role})",
            )
        return current_user
    return role_checker


# ==========================================
# 5. API Endpoints
# ==========================================

@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister) -> UserResponse:
    global user_id_counter
    if payload.username in users_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user_id_counter += 1
    user_in_db = UserInDB(
        id=user_id_counter,
        email=payload.email,
        username=payload.username,
        role=payload.role,
        hashed_password=hash_password(payload.password),
    )
    users_db[payload.username] = user_in_db
    return user_in_db


@app.post("/auth/login", response_model=TokenResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_jwt(user)
    return TokenResponse(access_token=token)


@app.get("/users/me", response_model=UserResponse)
def get_current_user_profile(user: Annotated[UserInDB, Depends(get_current_user)]) -> UserResponse:
    return user


@app.get("/admin/metrics", dependencies=[Depends(require_role(["admin"]))])
def get_admin_metrics() -> dict[str, object]:
    return {"total_users": len(users_db), "system_health": "OPTIMAL", "confidential_status": "SECURE"}
