"""Problem 01 — Binary Struct Network Protocol Header

Target: Production-grade implementation

Example:
    >>> b = pack_protocol_header(1, 1024, 0xAA55)
    >>> b
    b'\x00\x01\x00\x00\x04\x00\xaaU'
    >>> len(b)
    8
    >>> unpack_protocol_header(b)
    (1, 1024, 43605)

Hints:
    Hint 1: This is a fixed binary wire format, not JSON — each field has an
        exact byte width and byte order, and both functions must agree on
        that layout or round-tripping will silently misalign the fields.
    Hint 2: Use the `struct` module with a format string that fixes byte
        order and widths explicitly, then call `struct.pack`/`struct.unpack`
        with that same format string in both directions.
    Hint 3: The header is 8 bytes total: a 2-byte `msg_type`, a 4-byte
        `payload_len`, and a 2-byte `checksum`, all big-endian (`'>HIH'`) —
        get the format string's field order and byte widths wrong and
        `unpack_protocol_header` won't reproduce the original values.
"""

from __future__ import annotations


def pack_protocol_header(msg_type: int, payload_len: int, checksum: int) -> bytes:
    raise NotImplementedError('Implement pack_protocol_header')
def unpack_protocol_header(data: bytes) -> tuple[int, int, int]:
    raise NotImplementedError('Implement unpack_protocol_header')
