# Module 17: Troubleshooting, WebSockets & Middleware Traps

This reference guide details common errors and edge cases in advanced FastAPI systems.

---

## 1. WebSocket Client Disconnect Leak

### The Bug
```python
@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)
    while True:
        # If client closes browser tab, this throws WebSocketDisconnect!
        data = await ws.receive_text()
        # ❌ active_connections still holds dead socket object!
```

### The Fix
Always catch `WebSocketDisconnect` inside a `try/finally` block to remove the socket:
```python
from starlette.websockets import WebSocketDisconnect

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(ws) # ✅ Cleanly removed!
```

---

## 2. Yield Dependencies with Database Rollbacks

### The Rule
Ensure that if an endpoint raises an exception, the yield dependency catches it and performs a database `rollback()` before closing:
```python
async def get_db():
    session = AsyncSession()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
```
