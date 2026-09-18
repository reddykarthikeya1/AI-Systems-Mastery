"""Problem 01 — HTTP Chunked Transfer Decoder

Target: Production-grade implementation
"""

from __future__ import annotations


def parse_chunked_body(raw_bytes: bytes) -> bytes:
    out = bytearray()
    idx = 0
    while idx < len(raw_bytes):
        crlf = raw_bytes.find(b'\r\n', idx)
        if crlf == -1: break
        size_str = raw_bytes[idx:crlf].decode('ascii')
        size = int(size_str, 16)
        if size == 0: break
        idx = crlf + 2
        out.extend(raw_bytes[idx:idx+size])
        idx += size + 2
    return bytes(out)
