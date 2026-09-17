# 🐣 Interactive Foundations Playground: Advanced FastAPI: WebSockets & DI

> *"Dependency injection decouples application logic from transport and persistence layers."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from typing import Callable, Dict
```

---

## 1. Dependency Injection Container

A dependency injection container resolves component dependencies dynamically based on registered providers.

```python
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
```

---

## 2. Simulating WebSocket Full-Duplex Frames

WebSockets maintain persistent connections for streaming bidirectional text frames.

```python
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
```

---

## 3. Connection State Lifecycle

WebSocket connections transition through CONNECTING, OPEN, and CLOSED states.

```python
state = "CONNECTING"
state = "OPEN"
assert state == "OPEN"
state = "CLOSED"
assert state == "CLOSED"
print("Connection state machine transitions completed.")
```

---
