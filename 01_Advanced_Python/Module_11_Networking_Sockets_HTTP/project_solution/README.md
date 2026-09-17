# Design Rationale: Low-Level TCP Chat Server & HTTP Protocol Engine

## Architectural Overview
A high-throughput non-blocking TCP socket server and HTTP wire parser implementing length-prefixed protocol framing, socket option tuning, and resilient client connection management.

## Key Design Decisions
1. **Length-Prefixed Framing Protocol:** Prefixes every TCP message with a 4-byte big-endian integer, completely solving the continuous-stream TCP packet fragmentation problem.
2. **`SO_REUSEADDR` Socket Configuration:** Configured on the listening server socket to allow immediate port rebinding upon service restarts without waiting for `TIME_WAIT` expiration.
3. **Loop-Based Exact Byte Receives:** Sockets read in loops until expected payload lengths are met, preventing corrupted partial message deserialization.

## Rejected Alternatives
1. **Assuming `socket.send(data)` Transmits All Bytes:**
   - *Reason for Rejection:* Under network congestion, `socket.send()` transmits only a partial slice of the buffer. Failing to use `sendall()` causes silent packet truncation.
2. **Delimiter-Only Framing (`\n`) for Binary Data:**
   - *Reason for Rejection:* If the binary payload contains the newline character, the message boundary is prematurely split, corrupting the protocol stream.

## Invariants & Guarantees
- Packet framing integrity is guaranteed across arbitrary TCP fragmentation.
- Disconnected client sockets are deterministically pruned from connection registries.

## Verification
```bash
pytest test_chat_server.py -v
```

---

## 🗺️ Recommended Step-by-Step Project Study Path

Follow this sequence to analyze and master the project architecture:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Architecture Review** | Read the specification and design breakdown in this `README.md`. |
| **2** | **Examine Implementation** | Study modular design patterns and invariant safeguards across source files. |
| **3** | **Run Test Suite** | Execute `pytest tests/` to see all production test cases pass green. |
| **4** | **Independent Re-Build** | Re-implement the solution from scratch in `[../starter/](../starter/)` until all tests pass. |

