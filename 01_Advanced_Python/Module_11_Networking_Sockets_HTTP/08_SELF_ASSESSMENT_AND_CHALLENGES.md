# Module 11: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Network Sockets, TCP/UDP, and HTTP internals before moving to **Module 11**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Protocol Fundamentals:** What is the technical difference between TCP (Transmission Control Protocol) and UDP (User Datagram Protocol)?
2. **Addressing:** In the socket address tuple `("127.0.0.1", 8080)`, what role is played by the IP address vs the Port number?
3. **TCP Handshake:** Describe the 3 packets exchanged during the initial TCP connection handshake.
4. **Port Rebinding:** What error occurs when restarting a server without `SO_REUSEADDR`, and why does the OS enforce `TIME_WAIT`?
5. **Stream Boundaries:** Why can you not assume that `sock.send(b"Hello")` will be received in a single `sock.recv()` call on the other end?
6. **HTTP Framing:** What exact character sequence signals the end of HTTP/1.1 headers and the beginning of the message body?
7. **Multiplexing:** How does HTTP/2 solve the "Head-of-Line Blocking" problem present in HTTP/1.1?
8. **Asynchronous Sockets:** How does `asyncio.start_server()` handle thousands of simultaneous client connections on a single thread?
9. **Connection Lifecycle:** What does receiving `b""` (empty bytes) from a `sock.recv()` call signify?
10. **Transport Security:** What layer in the OSI model does TLS/SSL operate at to encrypt raw socket traffic?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- **TCP:** Connection-oriented, guarantees packet ordering, retransmits lost packets, and provides error checking (ideal for HTTP, databases, file transfers).
- **UDP:** Connectionless, unordered, no retransmission guarantee, minimal latency overhead (ideal for live video streaming, DNS, multiplayer gaming).

#### Answer 2:
- **IP Address:** Identifies the host machine on the network.
- **Port:** Identifies the specific application/process listening on that host.

#### Answer 3:
1. **SYN:** Client sends synchronization packet to request connection.
2. **SYN-ACK:** Server acknowledges and sends its own synchronization packet.
3. **ACK:** Client confirms receipt; socket connection enters `ESTABLISHED` state.

#### Answer 4:
`OSError: Address already in use`. The OS holds ports in `TIME_WAIT` to ensure delayed or duplicate packets in transit do not corrupt a new connection. `SO_REUSEADDR` allows immediate reuse.

#### Answer 5:
TCP is a continuous stream of bytes, not a sequence of independent messages. Packets may be split, merged, or buffered by routers and network cards.

#### Answer 6:
`\r\n\r\n` (CRLF CRLF / double carriage return line feed).

#### Answer 7:
HTTP/2 breaks requests and responses down into independent binary frames and multiplexes them over a single shared TCP connection, preventing slow requests from blocking others.

#### Answer 8:
It uses OS kernel event notifications (`epoll` on Linux, `kqueue` on macOS, `I/O Completion Ports (IOCP)` on Windows) to wake up coroutines only when network sockets have bytes ready to read.

#### Answer 9:
An empty byte return (`b""`) indicates that the remote peer has **cleanly closed or disconnected** the connection (received TCP FIN packet).

#### Answer 10:
TLS operates between the **Transport Layer (Layer 4 - TCP)** and the **Application Layer (Layer 7 - HTTP)**.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Non-Blocking Port Connectivity Checker

**Goal:** Write a function `is_port_open(host: str, port: int, timeout: float = 0.5) -> bool` using Python's `socket` module.

<details>
<summary><b>Solution Code</b></summary>

```python
import socket

def is_port_open(host: str, port: int, timeout: float = 0.5) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        return result == 0  # 0 indicates successful connection

# Verification:
print("Is localhost port 80 open?:", is_port_open("127.0.0.1", 80))
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Assuming one recv equals one message

```python
import socket

def receive(sock: socket.socket) -> str:
    data = sock.recv(1024)
    return data.decode()
```

**Observed symptom:** Sometimes returns half a message; sometimes two messages concatenated. Works fine on localhost, fails over the internet.

**(a)** Why can one `recv` return partial or multiple messages?

**(b)** What are the two standard framing solutions?

**(c)** Why does localhost hide the bug?

<details>
<summary><b>Show the diagnosis</b></summary>

TCP is a **byte stream**, not a message protocol. It guarantees order and delivery, never that your logical message boundaries survive. The kernel coalesces small sends (Nagle) and splits large ones at the MTU.

**Framing, two options:** (1) **length prefix** — send a fixed-width big-endian length, then read exactly that many bytes in a loop; (2) **delimiter** — terminate with `\n` and buffer until you see one, which requires escaping the delimiter in payloads.

**Localhost hides it** because there is no real MTU, no fragmentation, and near-zero latency, so a small message almost always arrives in one piece. The bug appears the moment there is a real network between the peers — that is, in production.

</details>

---

### D2. recv returns fewer bytes than requested

```python
def read_exactly(sock, n: int) -> bytes:
    return sock.recv(n)
```

**Observed symptom:** Occasionally returns short data and the caller misparses the record.

**(a)** What does the `n` in `recv(n)` actually mean?

**(b)** Write the correct loop.

**(c)** What does an empty `bytes` return signify?

<details>
<summary><b>Show the diagnosis</b></summary>

`recv(n)` reads **at most** `n` bytes — whatever is available in the socket buffer right now. It is not a promise to fill your buffer.

**Correct:**

```python
def read_exactly(sock, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError('peer closed early')
        buf += chunk
    return bytes(buf)
```

**Empty bytes (`b''`)** means the peer performed an orderly shutdown — EOF. It is not an error and not 'no data yet'; a non-blocking socket with no data raises `BlockingIOError` instead. Conflating the two is how you get a busy-loop that pegs a core.

</details>

---

### D3. Address already in use

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 8080))
server.listen()
```

**Observed symptom:** After stopping and immediately restarting the server: `OSError: [Errno 98] Address already in use`.

**(a)** Why is the port still held when the process has exited?

**(b)** What is the fix, and where must it go?

**(c)** When is that fix *unsafe*?

<details>
<summary><b>Show the diagnosis</b></summary>

The previous listening socket's connections are in **TIME_WAIT**, a mandatory 2×MSL wait (typically 30–120 s) that lets delayed duplicate packets drain before the 4-tuple can be reused.

**Fix:** `server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` — and it must be set **before** `bind()`, or it has no effect.

**Unsafe when:** you actually have multiple processes racing to bind the same port and expect only one to win — `SO_REUSEADDR` can mask a real misconfiguration. `SO_REUSEPORT` is the deliberate load-balancing tool for that, and it has different semantics. For a dev server, `SO_REUSEADDR` is correct and standard.

</details>

---

### D4. No timeout on a socket

```python
import socket

sock = socket.create_connection(("example.com", 80))
sock.sendall(b"GET / HTTP/1.0\r\n\r\n")
body = sock.recv(65536)
```

**Observed symptom:** The process hangs indefinitely when the peer is unresponsive. No error, no log, no exit.

**(a)** Which two distinct operations can block forever here?

**(b)** How do you bound each?

**(c)** Why is an application-level timeout still needed even with TCP keepalive?

<details>
<summary><b>Show the diagnosis</b></summary>

Both the **connect** and the **recv** can block without limit. A silently dropped packet stream produces no error at all — the socket simply never becomes readable.

**Bound them:** `socket.create_connection(addr, timeout=5)` sets both the connect timeout and the default socket timeout; `sock.settimeout(10)` adjusts it afterwards. A timeout raises `socket.timeout` (an `OSError` subclass), which you must handle.

**Keepalive is not enough:** TCP keepalive defaults to *two hours* of idle time before the first probe on Linux, and it detects a dead *connection*, not a slow or hung *application* that keeps the socket open and never replies. Always set an application-level deadline for the whole operation.

</details>

---

### D5. HTTP parsing by string splitting

```python
def parse_status(raw: bytes) -> int:
    first_line = raw.split(b"\n")[0]
    return int(first_line.split(b" ")[1])
```

**Observed symptom:** Works against one server, raises `IndexError` or `ValueError` against another.

**(a)** Name three ways a valid HTTP response breaks this parser.

**(b)** What should you use instead?

**(c)** What is the security risk of a hand-rolled parser here?

<details>
<summary><b>Show the diagnosis</b></summary>

**Three breakages:** (1) HTTP uses `\r\n`, so `first_line` retains a trailing `\r` and the split shifts; (2) the reason phrase is optional, and multiple spaces are legal, so field positions vary; (3) the response may arrive across several `recv` calls, so `raw` may not contain a complete first line at all.

**Use instead:** `h11` or `httptools` for a correct low-level parser, or `httpx`/`requests` at the application level. Writing HTTP by hand is a teaching exercise, not a production strategy.

**Security risk:** inconsistent parsing between your code and an upstream proxy is the basis of **request smuggling** — the proxy and the server disagree about where one request ends and the next begins, letting an attacker inject a request into another user's connection. Header and length parsing is exactly where this happens.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
