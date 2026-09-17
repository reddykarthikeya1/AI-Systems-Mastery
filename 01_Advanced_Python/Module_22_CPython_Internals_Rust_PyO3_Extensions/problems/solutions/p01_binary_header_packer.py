"""Problem 01 — Binary Struct Network Protocol Header

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


import struct

def pack_protocol_header(msg_type: int, payload_len: int, checksum: int) -> bytes:
    # Big-endian: uint16 msg_type, uint32 payload_len, uint16 checksum
    return struct.pack('>HIH', msg_type, payload_len, checksum)

def unpack_protocol_header(data: bytes) -> tuple[int, int, int]:
    return struct.unpack('>HIH', data)
