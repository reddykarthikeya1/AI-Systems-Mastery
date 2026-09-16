# Module_17_Advanced_FastAPI_WebSockets_DI: Project Implementation Guide

**Deliverable:** a real-time WebSocket communication server with channel isolation, custom ASGI telemetry middleware, and yield dependency injection.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_chat_api.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — WebSocket Connection Manager
Implement `ConnectionManager` tracking active connections partitioned by room name.

### Step 2 — Room Broadcasting
Implement `broadcast_room(room, message, exclude)` sending messages across all connected clients in a specific room.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_chat_api.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Telemetry Middleware
Implement HTTP middleware injecting `X-Correlation-ID` and measuring `X-Response-Time-Ms`.

### Step 4 — Yield Dependency Auditing
Implement `get_audit_logger` recording transaction entry and exit using `yield`.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/chat_api.py`, remove room partitioning so `broadcast_room` sends messages to all connected sockets across all rooms.
Run:
```bash
pytest ../project_solution/test_chat_api.py -k test_websocket_room_isolation -v
```
Watch the test fail when room Alpha messages leak into room Beta, then restore room isolation.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_chat_api.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Redis Pub/Sub Multi-Node Scale:** Scale WebSocket broadcasting across multiple servers using Redis Pub/Sub.
2. **WebSocket Heartbeat & Reconnection:** Implement ping/pong frames to drop stale connections.
3. **Binary Document Delta Sync:** Transmit binary CRDT or diff patches over WebSocket binary frames.
4. **Presence Indicators:** Broadcast real-time typing indicators and online user counts.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_middleware_and_yield_dependency` | Proves telemetry headers and audit dependency execution |
| `test_websocket_room_broadcasting` | Proves connected clients in the same room receive broadcasts |
| `test_websocket_room_isolation` | Proves messages in one room do not leak into another room |
| `test_websocket_quit_command` | Proves sending /quit cleanly disconnects the client |
| `test_websocket_disconnect_cleans_manager` | Proves empty rooms are pruned when clients disconnect |

---

## 🎓 You have mastered this module when you can…

- [ ] Manage real-time persistent connections using FastAPI WebSocket endpoints
- [ ] Isolate message broadcasting by topic/room channels
- [ ] Clean up dead or disconnected WebSockets without interrupting other clients
- [ ] Write custom ASGI middleware to intercept requests and inject correlation headers
- [ ] Manage resource lifecycles using yield dependency injection in FastAPI
- [ ] Test WebSocket endpoints using Starlette TestClient websocket_connect
- [ ] Diagnose race conditions and deadlocks in concurrent state management
