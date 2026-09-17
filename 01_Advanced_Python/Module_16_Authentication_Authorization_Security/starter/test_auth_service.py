"""Unit tests for the Multi-Tenant RBAC Authentication Microservice."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt
import pytest
from auth_service import (
    JWT_ALGORITHM,
    JWT_SECRET,
    app,
    hash_password,
    users_db,
    verify_password,
)
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_users():
    users_db.clear()
    yield
    users_db.clear()


def test_user_registration_and_login_flow() -> None:
    # 1. Register User
    reg_payload = {
        "email": "alice@security.com",
        "username": "alice_sec",
        "password": "SecurePassword123!",
        "role": "admin",
    }
    res_reg = client.post("/auth/register", json=reg_payload)
    assert res_reg.status_code == 201
    assert res_reg.json()["username"] == "alice_sec"

    # 2. Login
    login_data = {"username": "alice_sec", "password": "SecurePassword123!"}
    res_login = client.post("/auth/login", data=login_data)
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]
    assert len(token) > 20

    # 3. Access Protected /users/me
    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/users/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["email"] == "alice@security.com"

    # 4. Access Admin Metrics (Alice is admin)
    res_admin = client.get("/admin/metrics", headers=headers)
    assert res_admin.status_code == 200
    assert res_admin.json()["system_health"] == "OPTIMAL"


def test_rbac_permission_denied_for_viewer() -> None:
    # 1. Register Viewer User
    client.post("/auth/register", json={
        "email": "bob@viewer.com",
        "username": "bob_viewer",
        "password": "ViewerPassword123!",
        "role": "viewer",
    })

    # 2. Login as Viewer
    res_login = client.post("/auth/login", data={"username": "bob_viewer", "password": "ViewerPassword123!"})
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Viewer accessing Admin Metrics -> 403 Forbidden
    res_admin = client.get("/admin/metrics", headers=headers)
    assert res_admin.status_code == 403
    assert "requires roles" in res_admin.json()["detail"]


def test_login_incorrect_password_returns_401() -> None:
    """Test login with wrong password returns 401 Unauthorized."""
    client.post("/auth/register", json={
        "email": "user@test.com",
        "username": "valid_user",
        "password": "CorrectPassword123!",
        "role": "viewer",
    })
    res = client.post("/auth/login", data={"username": "valid_user", "password": "WrongPassword!"})
    assert res.status_code == 401
    assert "Incorrect username or password" in res.json()["detail"]


def test_login_nonexistent_user_returns_401() -> None:
    """Test login with non-existent username returns 401."""
    res = client.post("/auth/login", data={"username": "ghost_user", "password": "AnyPassword123!"})
    assert res.status_code == 401


def test_duplicate_username_conflict_returns_409() -> None:
    """Test duplicate registration returns 409 Conflict."""
    payload = {
        "email": "first@test.com",
        "username": "same_username",
        "password": "Password12345!",
        "role": "viewer",
    }
    res1 = client.post("/auth/register", json=payload)
    assert res1.status_code == 201

    payload2 = {
        "email": "second@test.com",
        "username": "same_username",
        "password": "Password12345!",
        "role": "editor",
    }
    res2 = client.post("/auth/register", json=payload2)
    assert res2.status_code == 409


def test_registration_invalid_email_format_returns_422() -> None:
    """Test registration with malformed email triggers 422."""
    payload = {
        "email": "not-an-email",
        "username": "valid_name",
        "password": "Password12345!",
        "role": "viewer",
    }
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 422


def test_registration_short_password_returns_422() -> None:
    """Test password under 8 characters triggers 422."""
    payload = {
        "email": "short@test.com",
        "username": "short_user",
        "password": "short",
        "role": "viewer",
    }
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 422


def test_tampered_jwt_signature_returns_401() -> None:
    """Test tampered bearer token signature returns 401."""
    tampered_token = jwt.encode({"sub": "1", "username": "fake"}, "wrong-secret-key-at-least-32-bytes-long!!!", algorithm="HS256")
    res = client.get("/users/me", headers={"Authorization": f"Bearer {tampered_token}"})
    assert res.status_code == 401
    assert "Invalid token signature" in res.json()["detail"]


def test_expired_jwt_token_returns_401() -> None:
    """Test expired token returns 401 Token expired."""
    expired_payload = {
        "sub": "1",
        "username": "expired_user",
        "role": "viewer",
        "exp": datetime.now(UTC) - timedelta(minutes=10),
    }
    expired_token = jwt.encode(expired_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    res = client.get("/users/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert res.status_code == 401
    assert "Token expired" in res.json()["detail"]


def test_password_hashing_and_verification_helpers() -> None:
    """Test bcrypt hashing salt uniqueness and verification helper."""
    raw = "MySecretPassphrase99!"
    hash1 = hash_password(raw)
    hash2 = hash_password(raw)

    assert hash1 != hash2  # Unique salt per hash
    assert verify_password(raw, hash1)
    assert verify_password(raw, hash2)
    assert not verify_password("WrongPassword", hash1)


def test_unauthenticated_request_me_returns_401() -> None:
    """Test GET /users/me without Authorization header returns 401."""
    res = client.get("/users/me")
    assert res.status_code == 401
