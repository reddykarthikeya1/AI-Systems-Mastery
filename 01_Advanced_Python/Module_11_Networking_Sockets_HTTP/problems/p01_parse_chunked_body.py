"""Problem 01 — HTTP Chunked Transfer Decoder

Target: Production-grade implementation

Example:
    >>> parse_chunked_body(b'4\r\nWiki\r\n5\r\npedia\r\n0\r\n\r\n')
    b'Wikipedia'
    >>> parse_chunked_body(b'0\r\n\r\n')
    b''

Hints:
    Hint 1: Each chunk is self-describing — a hex length on its own line
        tells you exactly how many payload bytes follow, so you never need
        to guess where a chunk ends.
    Hint 2: Walk the byte string with an index, using `bytes.find(b'\r\n', idx)`
        to locate each size line, `int(size_str, 16)` to decode the length,
        and slice out that many payload bytes before advancing past the
        trailing `\r\n`.
    Hint 3: The size line is hex, not decimal, and a chunk of size `0`
        signals the end of the stream — stop there rather than trying to
        parse a size line past it (the final `\r\n\r\n` has no payload to
        extract).
"""

from __future__ import annotations


def parse_chunked_body(raw_bytes: bytes) -> bytes:
    raise NotImplementedError('Implement parse_chunked_body')
