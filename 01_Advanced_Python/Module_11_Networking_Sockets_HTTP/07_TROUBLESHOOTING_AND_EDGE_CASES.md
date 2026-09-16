# Module 11: Troubleshooting, Socket Traps & Network Edge Cases

This reference guide details common networking pitfalls when working with TCP sockets and HTTP connections in Python.

---

## 1. `OSError: [Errno 10048] Address already in use`

### The Bug
```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 8080)) # ❌ Crashes if server was restarted recently!
```

### Why It Happens
When a TCP socket closes, the operating system kernel holds the port in a `TIME_WAIT` state for 1–2 minutes to catch stray delayed packets.

### The Fix
Set the `SO_REUSEADDR` socket option before calling `bind()`:
```python
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 8080))
```

---

## 2. TCP Stream Fragmentation (The "Single Recv" Trap)

### The Bug
```python
# Assuming 10 KB data will arrive in one single recv() call:
data = sock.recv(10240) # ❌ Danger! TCP is a stream, not a packet container!
```

### Why It Happens
TCP does not preserve message boundaries. A 10 KB payload may arrive in 7 smaller chunks depending on router MTU sizes and network congestion.

### The Fix
Use **Message Framing**:
1. Prefix each message with its byte length (e.g. 4-byte integer length header).
2. Or use delimiter framing (e.g. terminating each message with `\r\n\r\n` or `\n`).
3. Loop `recv()` until the full declared payload length has been accumulated in memory.
