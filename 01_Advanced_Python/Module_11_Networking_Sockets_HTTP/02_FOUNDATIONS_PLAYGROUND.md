# 🐣 Interactive Foundations Playground: Networking: Sockets & HTTP Protocols

> *"Network protocols serialize application intents into byte streams across transport layers."*

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
from urllib.parse import parse_qs, urlparse
```

---

## 1. URL Parsing and Query Extraction

`urllib.parse` decomposes URI strings into scheme, host, path, and parameters.

```python
url = "https://api.example.com:8080/v1/query?service=search&page=2"
parsed = urlparse(url)
assert parsed.scheme == "https"
assert parsed.netloc == "api.example.com:8080"
assert parsed.path == "/v1/query"
params = parse_qs(parsed.query)
assert params["service"] == ["search"]
assert params["page"] == ["2"]
print(f"Parsed URL scheme: {parsed.scheme}, endpoint: {parsed.path}")
```

---

## 2. Simulating HTTP Request / Response Wire Protocol

HTTP/1.1 messages consist of status lines, key-value headers, and optional body bytes.

```python
raw_http = (
    b"HTTP/1.1 200 OK\r\n"
    b"Content-Type: application/json\r\n"
    b"Content-Length: 17\r\n"
    b"\r\n"
    b"{\"status\":\"ready\"}"
)
lines = raw_http.split(b"\r\n")
status_line = lines[0].decode()
headers = dict(line.decode().split(": ") for line in lines[1:3])
body = lines[4].decode()

assert "200 OK" in status_line
assert headers["Content-Type"] == "application/json"
assert body == '{"status":"ready"}'
print("HTTP wire protocol frame parsed successfully.")
```

---

## 3. Header Normalization and Status Codes

HTTP headers are case-insensitive and map cleanly into dictionary Lookups.

```python
normalized_headers = {k.lower(): v for k, v in [("X-Request-Id", "req-123"), ("Content-Type", "text/plain")]}
assert normalized_headers["x-request-id"] == "req-123"
assert "content-type" in normalized_headers
print(f"Normalized headers: {normalized_headers}")
```

---
