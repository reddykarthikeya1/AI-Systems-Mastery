"""Beginner playground for Module 11 - Networking: Sockets & HTTP Protocols.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from urllib.parse import parse_qs, urlparse

# -------------------------------------------- 1. URL Parsing and Query Extraction
url = "https://api.example.com:8080/v1/query?service=search&page=2"
parsed = urlparse(url)
assert parsed.scheme == "https"
assert parsed.netloc == "api.example.com:8080"
assert parsed.path == "/v1/query"
params = parse_qs(parsed.query)
assert params["service"] == ["search"]
assert params["page"] == ["2"]
print(f"Parsed URL scheme: {parsed.scheme}, endpoint: {parsed.path}")

# -------------------------------------------- 2. Simulating HTTP Request / Response Wire Protocol
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

# -------------------------------------------- 3. Header Normalization and Status Codes
normalized_headers = {k.lower(): v for k, v in [("X-Request-Id", "req-123"), ("Content-Type", "text/plain")]}
assert normalized_headers["x-request-id"] == "req-123"
assert "content-type" in normalized_headers
print(f"Normalized headers: {normalized_headers}")

print()
print("All checks passed.")
