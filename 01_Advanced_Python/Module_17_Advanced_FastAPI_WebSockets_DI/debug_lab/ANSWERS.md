# Debug Lab Answers: Module 17

<details>
<summary>Bug 1: Sequential unhandled broadcast to disconnected sockets</summary>

### Root Cause
Iterating through active WebSockets and awaiting `send_text()` without isolating exceptions means a single dropped client aborts the entire broadcast.

### Fix
Use `contextlib.suppress()` or `asyncio.gather(..., return_exceptions=True)` and clean up dead sockets:
```python
async def broadcast(self, message: str):
    dead = []
    for ws in list(self.active_sockets):
        try:
            await ws.send_text(message)
        except Exception:
            dead.append(ws)
    for d in dead:
        self.disconnect(d)
```
</details>
