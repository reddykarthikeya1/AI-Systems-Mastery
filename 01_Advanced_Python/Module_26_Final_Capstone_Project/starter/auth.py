"""STARTER - Module 26: Final Capstone Project

Authentication, Bcrypt Hashing, and JWT RBAC for Capstone Platform.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_auth.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/auth.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
from datetime import UTC, datetime, timedelta
from typing import Annotated
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
JWT_SECRET = "production-capstone-secret-jwt-key-256bit-enterprise"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field("viewer", pattern="^(admin|manager|viewer)$")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def hash_password(password: str) -> str:
    # [Tier 2] Algorithm: Implement hash_password adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_auth_hash_and_verify_password
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 26: implement hash_password()")


def verify_password(plain: str, hashed: str) -> bool:
    # [Tier 2] Algorithm: Implement verify_password adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_auth_hash_and_verify_password
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 26: implement verify_password()")


def create_access_token(user_id: int, username: str, role: str) -> str:
    # [Tier 2] Algorithm: Implement create_access_token adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_auth_create_and_decode_jwt_token
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 26: implement create_access_token()")


def get_current_user_claims(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    # [Tier 1] Algorithm: Implement get_current_user_claims adhering to the
    #   contract defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_analytics_aggregate_project_budgets
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 26: implement get_current_user_claims()")
