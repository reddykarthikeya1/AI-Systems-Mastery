#!/usr/bin/env python3
"""Module 10: HTTP Protocol Parsing Demonstration.

This script demonstrates formatting raw HTTP request bytes and parsing
the HTTP response envelope.
"""

from __future__ import annotations


def format_raw_http_get(host: str, path: str = "/") -> bytes:
    """Constructs raw HTTP/1.1 request wire bytes."""
    request_str = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: Python-Custom-Client/1.0\r\n"
        f"Accept: application/json, text/html\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return request_str.encode("utf-8")


def main() -> None:
    print("=" * 60)
    print("  HTTP/1.1 Raw Wire Frame Construction")
    print("=" * 60)

    raw_bytes = format_raw_http_get("api.example.com", "/v1/users?limit=10")
    print("Raw Bytes formatted for TCP Socket:\n")
    print(raw_bytes.decode("utf-8"))


if __name__ == "__main__":
    main()
