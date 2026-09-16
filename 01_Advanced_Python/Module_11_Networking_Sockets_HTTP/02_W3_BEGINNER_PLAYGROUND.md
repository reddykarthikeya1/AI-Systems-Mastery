# W3Schools-Style Playground: Networking, Sockets & HTTP

> *"A socket is a phone call between two computers; HTTP is the language they speak."*

Welcome to the **Module 11 Networking Sockets HTTP** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Computers communicate across networks using **Sockets**. A Server opens a socket and listens on a port; a Client connects to that IP and port. HTTP is a text-based protocol built on top of TCP sockets.

---

## 2. Micro-Code Example (3-5 Lines)

```python
import socket

# Create a TCP IPv4 socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to a host on port 80 (HTTP)
s.connect(("example.com", 80))
# Send raw HTTP request bytes
req = "GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
s.sendall(req.encode("utf-8"))
response = s.recv(512)
print(response.decode("utf-8", errors="ignore")[:100])
s.close()
```

### Line-by-Line Breakdown:
- `socket.AF_INET`: Specifies IPv4 addressing.
- `socket.SOCK_STREAM`: Specifies TCP (reliable, ordered stream of bytes).
- `.encode('utf-8')`: Converts text to raw bytes before transmitting over the network.
- `\r\n\r\n`: The standard HTTP blank line signaling that request headers are complete.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
Why must you use `.encode()` before sending data through a socket?

<details><summary><b>Show Answer</b></summary>

Physical networks only transmit binary bytes, not Python string objects.
</details>

---

### Drill 2: Quick Check
What is the difference between TCP and UDP?

<details><summary><b>Show Answer</b></summary>

TCP guarantees reliable, ordered packet delivery with handshakes; UDP sends packets without connection guarantees for lower latency (e.g. video streaming).
</details>

---
