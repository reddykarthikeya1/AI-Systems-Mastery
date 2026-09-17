"""Problem 01 — Binary Struct Network Protocol Header

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def pack_protocol_header(msg_type: int, payload_len: int, checksum: int) -> bytes:
    raise NotImplementedError('Implement pack_protocol_header')
def unpack_protocol_header(data: bytes) -> tuple[int, int, int]:
    raise NotImplementedError('Implement unpack_protocol_header')
