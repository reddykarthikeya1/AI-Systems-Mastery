#!/usr/bin/env python3
"""Production-Grade Fully Typed Python SDK Library.

Module 21 (Strict Typing & Packaging) Turnkey Project Implementation.
Demonstrates Generic[T], typing.Protocol, and type-safe response wrappers.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")
R = TypeVar("R")


@dataclass(frozen=True)
class ApiResponse(Generic[T]):
    """Type-safe immutable API response envelope."""
    status_code: int
    data: T | None = None
    error_message: str | None = None

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300


@runtime_checkable
class TransportProtocol(Protocol):
    """Protocol for mockable HTTP transport clients."""
    def send_request(self, method: str, endpoint: str, payload: dict | None = None) -> dict[str, Any]:
        ...


class MockHTTPTransport:
    """Mock implementation satisfying TransportProtocol."""
    def __init__(self, responses: dict[str, dict[str, Any]] | None = None) -> None:
        self.responses = responses or {
            "/v1/users/1": {"id": 1, "username": "alice_sdk", "tier": "enterprise"},
            "/v1/health": {"status": "HEALTHY"},
        }

    def send_request(self, method: str, endpoint: str, payload: dict | None = None) -> dict[str, Any]:
        if endpoint in self.responses:
            return self.responses[endpoint]
        raise LookupError(f"404 Endpoint Not Found: {endpoint}")


class TypedEnterpriseClient:
    """Fully typed enterprise API client."""

    def __init__(self, transport: TransportProtocol) -> None:
        self.transport = transport

    def get_resource(self, endpoint: str, transform: Callable[[dict[str, Any]], T]) -> ApiResponse[T]:
        try:
            raw_data = self.transport.send_request("GET", endpoint)
            typed_data = transform(raw_data)
            return ApiResponse(status_code=200, data=typed_data)
        except LookupError as err:
            return ApiResponse(status_code=404, error_message=str(err))
        except Exception as err:
            return ApiResponse(status_code=500, error_message=str(err))


@dataclass
class UserDTO:
    id: int
    username: str
    tier: str


def parse_user(payload: dict[str, Any]) -> UserDTO:
    return UserDTO(
        id=payload["id"],
        username=payload["username"],
        tier=payload["tier"],
    )


def main() -> None:
    print("=" * 65)
    print("      FULLY TYPED PYTHON SDK & PROTOCOLS DEMO")
    print("=" * 65)

    transport = MockHTTPTransport()
    client = TypedEnterpriseClient(transport)

    resp: ApiResponse[UserDTO] = client.get_resource("/v1/users/1", parse_user)
    if resp.is_success and resp.data:
        print("Fetch Successful!")
        print(f"User ID   : {resp.data.id}")
        print(f"Username  : {resp.data.username}")
        print(f"Tier      : {resp.data.tier}")


if __name__ == "__main__":
    main()
