#!/usr/bin/env python3
"""Real-Time Collaborative Document & WebSocket Chat API.

Module 15 (Advanced FastAPI & WebSockets) Turnkey Project Implementation.
Demonstrates ConnectionManager, Room-based WebSocket broadcasting,
custom correlation ID middleware, and yield dependency state management.
"""

from __future__ import annotations

import contextlib
import time
import uuid
from collections import defaultdict
from collections.abc import AsyncGenerator

from fastapi import Depends, FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

# ==========================================
# 1. Connection Manager for WebSockets
# ==========================================

class ConnectionManager:
    """Manages active WebSocket connections partitioned by chat room."""

    def __init__(self) -> None:
        # room_name -> list of (username, WebSocket)
        self.rooms: dict[str, list[tuple[str, WebSocket]]] = defaultdict(list)

    async def connect(self, room: str, username: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.rooms[room].append((username, websocket))
        await self.broadcast_room(room, f"[SYSTEM] {username} joined the room.", exclude=websocket)

    def disconnect(self, room: str, username: str, websocket: WebSocket) -> None:
        self.rooms[room] = [(u, ws) for u, ws in self.rooms[room] if ws != websocket]
        if not self.rooms[room]:
            del self.rooms[room]

    async def broadcast_room(self, room: str, message: str, exclude: WebSocket | None = None) -> None:
        for _username, ws in list(self.rooms.get(room, [])):
            if ws != exclude and ws.client_state == WebSocketState.CONNECTED:
                with contextlib.suppress(Exception):
                    await ws.send_text(message)


manager = ConnectionManager()
app = FastAPI(title="Real-Time Collaborative WebSocket API", version="1.0.0")


# ==========================================
# 2. Custom ASGI Telemetry Middleware
# ==========================================

@app.middleware("http")
async def correlation_id_and_timing_middleware(request: Request, call_next) -> Response:
    corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    start = time.perf_counter()

    response: Response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Correlation-ID"] = corr_id
    response.headers["X-Response-Time-Ms"] = f"{duration_ms:.2f}"
    return response


# ==========================================
# 3. Yield Dependency for Request Auditing
# ==========================================

audit_trail: list[str] = []


def get_audit_logger() -> AsyncGenerator[list[str], None]:
    audit_trail.append("[START] Transaction initialized")
    try:
        yield audit_trail
    finally:
        audit_trail.append("[COMPLETE] Transaction committed & closed")


# ==========================================
# 4. HTTP & WebSocket Endpoints
# ==========================================

@app.get("/rooms")
def list_active_rooms(audit=Depends(get_audit_logger)) -> dict[str, list[str]]:
    return {room: [u for u, _ in conns] for room, conns in manager.rooms.items()}


@app.websocket("/ws/{room}/{username}")
async def websocket_room_endpoint(websocket: WebSocket, room: str, username: str) -> None:
    await manager.connect(room, username, websocket)
    try:
        while True:
            text = await websocket.receive_text()
            if text.lower() == "/quit":
                break
            await manager.broadcast_room(room, f"[{username}] {text}")
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(room, username, websocket)
        await manager.broadcast_room(room, f"[SYSTEM] {username} left the room.")
