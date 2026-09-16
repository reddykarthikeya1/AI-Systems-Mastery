#!/usr/bin/env python3
"""Module 11: FastAPI Path & Query Parameter Routing Demonstration.

This script demonstrates FastAPI endpoints, type annotations, and testing
with TestClient.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI(title="Routing Demo")


class UserProfile(BaseModel):
    username: str
    email: str
    is_active: bool = True


users_db: dict[int, UserProfile] = {
    1: UserProfile(username="alice", email="alice@test.com"),
    2: UserProfile(username="bob", email="bob@test.com"),
}


@app.get("/users/{user_id}", response_model=UserProfile)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User #{user_id} not found")
    return users_db[user_id]


def main() -> None:
    print("=" * 60)
    print("  FastAPI Routing and HTTP Status Codes Demo")
    print("=" * 60)

    client = TestClient(app)

    # 1. Successful lookup
    res = client.get("/users/1")
    print(f"GET /users/1 -> Status: {res.status_code}, Body: {res.json()}")

    # 2. 404 lookup
    res_404 = client.get("/users/999")
    print(f"GET /users/999 -> Status: {res_404.status_code}, Body: {res_404.json()}")


if __name__ == "__main__":
    main()
