# Module_11_Networking_Sockets_HTTP: Project Implementation Guide

**Deliverable:** a production-grade async TCP chat server supporting room broadcasting, client presence, framing, and clean shutdown.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_chat_server.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Socket Server Initialization
Implement `AsyncChatServer(host, port)` initializing `asyncio.start_server` with `SO_REUSEADDR` enabled.

### Step 2 — Client Connection & Welcome
In `handle_client(reader, writer)`, accept connections, record client address, and send a welcome greeting.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_chat_server.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Delimited Message Framing
Read stream data using `reader.readline()` ensuring newline-delimited framing isolates discrete messages.

### Step 4 — Multi-Client Broadcasting
Maintain a thread-safe registry of connected writers and broadcast messages to all active clients except sender.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/chat_server.py`, remove the `except` block in the client loop and let client disconnects raise `ConnectionResetError`.
Run:
```bash
pytest ../project_solution/test_chat_server.py -k test_client_disconnect_leaves_room_notification -v
```
Watch the server crash on client disconnect instead of gracefully broadcasting departure, then restore cleanup.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_chat_server.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Binary Length-Prefixed Protocol:** Refactor from newline delimiter to 4-byte big-endian length prefixing.
2. **TLS / SSL Encryption:** Secure the socket connection using an `ssl.SSLContext`.
3. **Heartbeat Keep-Alive:** Send ping packets every 30s and evict unresponsive clients.
4. **Chat Rooms / Channels:** Allow clients to join named channels (`/join #python`) with partitioned broadcasts.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_chat_server_connection_and_broadcast` | Proves clients exchange messages across the TCP broadcast |
| `test_client_quit_command` | Proves sending /quit cleanly closes connection and writer |
| `test_server_custom_host_and_port` | Proves host and port configuration parameters are respected |
| `test_client_count_in_welcome_message` | Proves welcome messages reflect accurate active connection counts |
| `test_client_disconnect_leaves_room_notification` | Proves dropped connections notify remaining users |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain the difference between TCP byte-streams and message-oriented protocols
- [ ] Implement newline or length-prefixed framing to prevent message fragmentation bugs
- [ ] Use SO_REUSEADDR to avoid TIME_WAIT address binding conflicts on server restarts
- [ ] Manage concurrent async TCP connections using asyncio.StreamReader and StreamWriter
- [ ] Implement non-blocking broadcast mechanisms across registered socket writers
- [ ] Handle unexpected client drops and socket resets gracefully
- [ ] Write integration tests verifying network communication over localhost
