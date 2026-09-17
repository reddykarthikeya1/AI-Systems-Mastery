"""Beginner playground for Module 17 - Advanced FastAPI: WebSockets & DI.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from typing import Callable, Dict

# -------------------------------------------- 1. Dependency Injection Container
class Container:
    def __init__(self):
        self._services: Dict[str, Callable] = {}

    def register(self, key, provider):
        self._services[key] = provider

    def resolve(self, key):
        return self._services[key]()

c = Container()
c.register("db_url", lambda: "sqlite:///:memory:")
c.register("service_name", lambda: "payment_gateway")

assert c.resolve("db_url") == "sqlite:///:memory:"
assert c.resolve("service_name") == "payment_gateway"
print("Dependency injection container resolved registered services.")

# -------------------------------------------- 2. Simulating WebSocket Full-Duplex Frames
inbox = []
outbox = []

def send_ws_frame(frame):
    outbox.append(frame)

def recv_ws_frame(frame):
    inbox.append(frame)

send_ws_frame({"type": "subscribe", "channel": "ticker"})
recv_ws_frame({"type": "price_update", "val": 42.5})

assert len(outbox) == 1
assert len(inbox) == 1
assert inbox[0]["val"] == 42.5
print(f"WebSocket exchange completed: out={outbox[0]['type']}, in={inbox[0]['type']}")

# -------------------------------------------- 3. Connection State Lifecycle
state = "CONNECTING"
state = "OPEN"
assert state == "OPEN"
state = "CLOSED"
assert state == "CLOSED"
print("Connection state machine transitions completed.")

print()
print("All checks passed.")
