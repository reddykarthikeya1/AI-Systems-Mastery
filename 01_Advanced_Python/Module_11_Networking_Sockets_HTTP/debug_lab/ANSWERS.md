# Debug Lab Answers: Module 11

<details>
<summary>Bug 1: Missing SO_REUSEADDR socket option</summary>

### Root Cause
When a TCP socket closes, it enters the `TIME_WAIT` state for 1–4 minutes to ensure in-flight packets are drained. By default, the OS prevents rebinding to the same port.

### Fix
Set `SO_REUSEADDR` before calling `bind()`:
```python
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 9999))
```
</details>

<details>
<summary>Bug 2 & 3: Missing framing delimiter (TCP streaming nature)</summary>

### Root Cause
TCP is a byte-stream protocol, not a message protocol. There is no concept of a "packet boundary" at the application layer. Multiple `sendall()` calls can be merged (Nagle's algorithm) or fragmented across multiple `recv()` calls.

### Fix
Implement explicit framing, such as newline termination (`\n`) or length-prefixing:
```python
# Length-prefixed framing:
payload = msg.encode("utf-8")
length_prefix = len(payload).to_bytes(4, byteorder="big")
sock.sendall(length_prefix + payload)
```
</details>
