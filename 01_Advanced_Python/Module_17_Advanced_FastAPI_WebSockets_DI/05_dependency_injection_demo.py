#!/usr/bin/env python3
"""Module 15: FastAPI Dependency Injection Tree & Classes Demo.

This script demonstrates class-based dependencies and multi-level dependency trees.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI
from starlette.testclient import TestClient

app = FastAPI()


class PaginationParams:
    """Class-based dependency for standard limit/offset pagination."""
    def __init__(self, skip: int = 0, limit: int = 20) -> None:
        self.skip = skip
        self.limit = max(1, min(100, limit))


def verify_api_token(token: str = "default_token") -> str:
    """Sub-dependency verifying request token."""
    return token.upper()


def get_current_context(
    token: Annotated[str, Depends(verify_api_token)],
    pagination: Annotated[PaginationParams, Depends()],
) -> dict:
    """Composite dependency assembling sub-dependencies."""
    return {
        "auth_token": token,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@app.get("/items")
def list_items(ctx: Annotated[dict, Depends(get_current_context)]):
    return {"status": "success", "context": ctx}


def main() -> None:
    print("=" * 60)
    print("  FastAPI Multi-Level Dependency Tree Demonstration")
    print("=" * 60)

    client = TestClient(app)
    res = client.get("/items?skip=10&limit=50&token=secret_abc")
    print("Endpoint Result:\n", res.json())


if __name__ == "__main__":
    main()
