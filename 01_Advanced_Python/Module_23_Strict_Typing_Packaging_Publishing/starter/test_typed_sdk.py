"""Unit tests for the Typed SDK Library."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from typed_sdk import (
    ApiResponse,
    MockHTTPTransport,
    TransportProtocol,
    TypedEnterpriseClient,
    UserDTO,
    parse_user,
)


def test_transport_protocol_conformance() -> None:
    transport = MockHTTPTransport()
    assert isinstance(transport, TransportProtocol)


def test_typed_client_successful_fetch() -> None:
    transport = MockHTTPTransport()
    client = TypedEnterpriseClient(transport)

    resp = client.get_resource("/v1/users/1", parse_user)
    assert resp.is_success
    assert resp.status_code == 200
    assert resp.data is not None
    assert isinstance(resp.data, UserDTO)
    assert resp.data.username == "alice_sdk"


def test_typed_client_404_error_handling() -> None:
    transport = MockHTTPTransport()
    client = TypedEnterpriseClient(transport)

    resp = client.get_resource("/v1/nonexistent", parse_user)
    assert not resp.is_success
    assert resp.status_code == 404
    assert "Endpoint Not Found" in (resp.error_message or "")


def test_api_response_is_success_property() -> None:
    """Test is_success logic across 2xx, 4xx, and 5xx status codes."""
    assert ApiResponse(status_code=200).is_success
    assert ApiResponse(status_code=201).is_success
    assert ApiResponse(status_code=204).is_success
    assert not ApiResponse(status_code=400).is_success
    assert not ApiResponse(status_code=404).is_success
    assert not ApiResponse(status_code=500).is_success


def test_api_response_immutability() -> None:
    """Test ApiResponse is a frozen dataclass and prevents attribute mutation."""
    resp = ApiResponse(status_code=200, data="payload")
    with pytest.raises(FrozenInstanceError):
        resp.status_code = 400  # type: ignore


def test_mock_http_transport_custom_responses() -> None:
    """Test configuring custom responses dictionary in MockHTTPTransport."""
    custom = {"/api/custom": {"id": 99, "username": "custom_user", "tier": "pro"}}
    transport = MockHTTPTransport(responses=custom)
    res = transport.send_request("GET", "/api/custom")
    assert res["username"] == "custom_user"


def test_mock_http_transport_missing_endpoint_raises_lookup_error() -> None:
    """Test MockHTTPTransport raises LookupError for unrecognized routes."""
    transport = MockHTTPTransport({})
    with pytest.raises(LookupError, match="404 Endpoint Not Found"):
        transport.send_request("GET", "/unknown")


def test_typed_client_500_on_unexpected_exception() -> None:
    """Test client returns 500 ApiResponse when transform callable raises an unexpected error."""
    transport = MockHTTPTransport()
    client = TypedEnterpriseClient(transport)

    def faulty_transform(raw: dict) -> UserDTO:
        raise RuntimeError("Parsing crashed unexpectedly")

    resp = client.get_resource("/v1/users/1", faulty_transform)
    assert not resp.is_success
    assert resp.status_code == 500
    assert "Parsing crashed" in (resp.error_message or "")


def test_user_dto_parsing_and_field_integrity() -> None:
    """Test parse_user correctly maps dict keys to UserDTO fields."""
    raw = {"id": 42, "username": "bob_admin", "tier": "pro"}
    dto = parse_user(raw)
    assert dto.id == 42
    assert dto.username == "bob_admin"
    assert dto.tier == "pro"


def test_typed_client_generic_return_types() -> None:
    """Test TypedEnterpriseClient supports arbitrary transform return types."""
    transport = MockHTTPTransport()
    client = TypedEnterpriseClient(transport)

    # Transform returning int
    resp_int: ApiResponse[int] = client.get_resource("/v1/users/1", lambda r: int(r["id"]))
    assert resp_int.data == 1

    # Transform returning str
    resp_str: ApiResponse[str] = client.get_resource("/v1/health", lambda r: str(r["status"]))
    assert resp_str.data == "HEALTHY"
