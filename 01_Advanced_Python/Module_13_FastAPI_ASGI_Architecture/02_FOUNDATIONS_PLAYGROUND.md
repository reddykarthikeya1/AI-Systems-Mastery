# 🐣 Interactive Foundations Playground: FastAPI & ASGI Architecture

> *"ASGI standardizes asynchronous communication between Python web servers and applications."*

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
import json
```

---

## 1. ASGI Scope and Lifecycle Contract

An ASGI application is a coroutine accepting `scope`, `receive`, and `send` callables.

```python
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
```

---

## 2. ASGI Message Sending Simulation

Applications emit `http.response.start` and `http.response.body` messages through the `send` channel.

```python
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
```

---

## 3. Path Routing Resolution

FastAPI matches incoming URL paths against registered endpoint handlers.

```python
routes = {
    "/users": "user_handler",
    "/items": "item_handler"
}
assert routes.get("/users") == "user_handler"
assert routes.get("/missing") is None
print("Route table dispatched URL to handler successfully.")
```

---
