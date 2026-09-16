"""Authentication, Bcrypt Hashing, and JWT RBAC for Capstone Platform."""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# NEVER hard-code a signing key. Read it from the environment so production and
# development cannot share one, and so rotating it does not require a code change.
_DEV_SECRET = "dev-only-insecure-key-do-not-use-in-production"
JWT_SECRET = os.environ.get("CAPSTONE_JWT_SECRET", _DEV_SECRET)

if JWT_SECRET == _DEV_SECRET and os.environ.get("CAPSTONE_ENV") == "production":
    raise RuntimeError(
        "CAPSTONE_JWT_SECRET must be set when CAPSTONE_ENV=production. "
        "Refusing to start with the development signing key."
    )
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserRegisterSchema(BaseModel):
    """Public registration input.

    ``role`` is deliberately ABSENT. A field that a client can set and that the
    server uses for authorisation is a privilege-escalation vulnerability -
    the "mass assignment" (or over-posting) class of bug. Every new account is
    created as ``viewer``; promotion is an admin-only operation via
    ``/admin/users/{id}/role``.

    See Module 14's diagnostic D5 and Module 16's D4 for the same bug in
    isolation.
    """

    model_config = ConfigDict(extra="forbid")

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class RoleUpdateSchema(BaseModel):
    """Admin-only role change. Separate model, separate endpoint, separate authority."""

    model_config = ConfigDict(extra="forbid")

    role: str = Field(..., pattern="^(admin|manager|viewer)$")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: int, username: str, role: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user_claims(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature") from exc
