#!/usr/bin/env python3
"""Module 14: JWT Tokens & Role-Based Access Control (RBAC) Demonstration.

This script demonstrates generating and verifying signed JWT access tokens with
embedded user roles.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt

JWT_SECRET = "production-grade-hmac-secret-key-32-chars-long"
JWT_ALGORITHM = "HS256"


def create_access_token(user_id: int, role: str, expires_delta_minutes: int = 15) -> str:
    """Encodes a signed JWT bearer token."""
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta_minutes)
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_and_authorize(token: str, required_role: str) -> dict:
    """Decodes token and enforces role-based access control."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_role = payload.get("role")
        if user_role != required_role and user_role != "admin":
            raise PermissionError(f"User role '{user_role}' lacks required permission '{required_role}'")
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise ValueError("Token has expired!") from exc
    except jwt.InvalidTokenError as exc:
        raise ValueError("Invalid cryptographic token signature!") from exc


def main() -> None:
    print("=" * 60)
    print("  JWT Generation & RBAC Authorization Demo")
    print("=" * 60)

    admin_token = create_access_token(user_id=1, role="admin")
    viewer_token = create_access_token(user_id=2, role="viewer")

    print(f"Generated Admin Token : {admin_token[:30]}...")
    print(f"Generated Viewer Token: {viewer_token[:30]}...\n")

    # Authorize admin for 'editor' action (Admin has superset permissions)
    auth_admin = decode_and_authorize(admin_token, required_role="editor")
    print(f"Admin Authorization: SUCCESS (User #{auth_admin['sub']})")

    # Attempt to authorize viewer for 'editor' action
    try:
        decode_and_authorize(viewer_token, required_role="editor")
    except PermissionError as err:
        print(f"Viewer Authorization: REJECTED ({err})")


if __name__ == "__main__":
    main()
