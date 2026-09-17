"""Beginner playground for Module 13 - FastAPI & ASGI Architecture.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import json

# -------------------------------------------- 1. ASGI Scope and Lifecycle Contract
mock_scope = {
    "type": "http",
    "method": "GET",
    "path": "/api/health",
    "headers": [(b"host", b"localhost")]
}
assert mock_scope["type"] == "http"
assert mock_scope["method"] == "GET"
assert mock_scope["path"] == "/api/health"
print("ASGI scope dictionary validated.")

# -------------------------------------------- 2. ASGI Message Sending Simulation
sent_messages = []
async def mock_send(msg):
    sent_messages.append(msg)

import asyncio
async def minimal_asgi(scope, receive, send):
    await send({"type": "http.response.start", "status": 200})
    await send({"type": "http.response.body", "body": b'{"ok": true}'})

asyncio.run(minimal_asgi(mock_scope, None, mock_send))
assert len(sent_messages) == 2
assert sent_messages[0]["status"] == 200
assert sent_messages[1]["body"] == b'{"ok": true}'
print("ASGI simulated request finished with 200 OK.")

# -------------------------------------------- 3. Path Routing Resolution
routes = {
    "/users": "user_handler",
    "/items": "item_handler"
}
assert routes.get("/users") == "user_handler"
assert routes.get("/missing") is None
print("Route table dispatched URL to handler successfully.")

print()
print("All checks passed.")
