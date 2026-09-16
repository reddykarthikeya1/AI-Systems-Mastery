#!/usr/bin/env python3
"""Broken Auth Service demonstrating timing attacks and unverified expiration."""

import hmac
import time
from datetime import datetime, timedelta, timezone
import jwt

SECRET = "super-secret-production-key-at-least-32-bytes"

def insecure_token_verify(token: str) -> dict:
    # Expired tokens remain valid forever!
    return jwt.decode(token, SECRET, algorithms=["HS256"], options={"verify_exp": False})

def insecure_secret_comparison(user_input: str, actual_secret: str) -> bool:
    return user_input == actual_secret

if __name__ == "__main__":
    # Create an expired token
    expired_time = datetime.now(timezone.utc) - timedelta(days=365)
    expired_token = jwt.encode({"sub": "admin", "exp": expired_time}, SECRET, algorithm="HS256")

    claims = insecure_token_verify(expired_token)
    print(f"Expired token verified as valid! User: {claims['sub']}")

    match = insecure_secret_comparison("pass123", "pass123")
    print(f"Insecure comparison: {match}")
