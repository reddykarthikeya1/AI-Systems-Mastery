"""Unit tests for the Real-Time Collaborative Document & WebSocket Chat API."""

from __future__ import annotations

import pytest
from chat_api import app, audit_trail, manager
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_state():
    audit_trail.clear()
    manager.rooms.clear()
    yield
    audit_trail.clear()
    manager.rooms.clear()


def test_middleware_and_yield_dependency() -> None:
    custom_trace = "test-trace-999"
    res = client.get("/rooms", headers={"X-Correlation-ID": custom_trace})

    assert res.status_code == 200
    assert res.headers["X-Correlation-ID"] == custom_trace
    assert "X-Response-Time-Ms" in res.headers
    assert len(audit_trail) >= 2
    assert audit_trail[0].startswith("[START]")
    assert audit_trail[1].startswith("[COMPLETE]")


def test_websocket_room_broadcasting() -> None:
    with (
        client.websocket_connect("/ws/Engineering/Alice") as ws_alice,
        client.websocket_connect("/ws/Engineering/Bob") as ws_bob,
    ):
        joined_msg = ws_alice.receive_text()
        assert "Bob joined the room" in joined_msg

        ws_alice.send_text("Deploying v2.0 to staging!")

        assert "Deploying v2.0 to staging!" in ws_alice.receive_text()
        assert "Deploying v2.0 to staging!" in ws_bob.receive_text()


def test_middleware_generates_uuid_correlation_id() -> None:
    """Test middleware auto-generates correlation ID when none provided."""
    res = client.get("/rooms")
    assert res.status_code == 200
    assert "X-Correlation-ID" in res.headers
    assert len(res.headers["X-Correlation-ID"]) > 10


def test_middleware_duration_header_is_numeric() -> None:
    """Test X-Response-Time-Ms is numeric and non-negative."""
    res = client.get("/rooms")
    duration = float(res.headers["X-Response-Time-Ms"])
    assert duration >= 0.0


def test_list_active_rooms_initially_empty() -> None:
    """Test GET /rooms returns empty dictionary when no users connected."""
    res = client.get("/rooms")
    assert res.status_code == 200
    assert res.json() == {}


def test_rooms_endpoint_reflects_active_connections() -> None:
    """Test GET /rooms reflects rooms and connected usernames."""
    with client.websocket_connect("/ws/Operations/Charlie"):
        res = client.get("/rooms")
        assert res.status_code == 200
        data = res.json()
        assert "Operations" in data
        assert "Charlie" in data["Operations"]


def test_websocket_room_isolation() -> None:
    """Test messages broadcasted in one room do not leak into another room."""
    with (
        client.websocket_connect("/ws/Alpha/UserA") as ws_a,
        client.websocket_connect("/ws/Beta/UserB") as ws_b,
    ):
        ws_a.send_text("Confidential Alpha message")
        msg_a = ws_a.receive_text()
        assert "Confidential Alpha message" in msg_a

        # Send a message to Beta to ensure ws_b receives Beta message, not Alpha
        ws_b.send_text("Hello Beta")
        msg_b = ws_b.receive_text()
        assert "Hello Beta" in msg_b
        assert "Confidential Alpha" not in msg_b


def test_websocket_quit_command() -> None:
    """Test sending /quit cleanly closes connection."""
    with (
        client.websocket_connect("/ws/Lobby/Alice") as ws_alice,
        client.websocket_connect("/ws/Lobby/Bob") as ws_bob,
    ):
        # Consume Bob joined message
        ws_alice.receive_text()

        # Alice sends /quit
        ws_alice.send_text("/quit")

        # Bob receives departure notification
        leave_msg = ws_bob.receive_text()
        assert "Alice left the room" in leave_msg


def test_websocket_disconnect_cleans_manager_rooms() -> None:
    """Test room entry is purged from manager when the last user disconnects."""
    with client.websocket_connect("/ws/Ephemeral/Solo"):
        assert "Ephemeral" in manager.rooms
        assert len(manager.rooms["Ephemeral"]) == 1

    assert "Ephemeral" not in manager.rooms


@pytest.mark.asyncio
async def test_broadcast_room_empty_safe() -> None:
    """Test broadcasting to non-existent room does not raise exception."""
    await manager.broadcast_room("NonExistentRoom", "Hello")
