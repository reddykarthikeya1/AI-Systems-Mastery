"""Problem 01 — Rdb Snapshot Ziplist

Topic: 12 Redis Data Structures Persistence
Target: Production-grade implementation

Pack list of small integer and string values into compact simulated ziplist byte representation.

Example:
    >>> rdb_snapshot_ziplist(["redis", 42, "cache"])
    b'\x00\x00\x00\x15\x00\x03\x05redis\x0242\x05cache'

Hints:
    Hint 1: Every value, whether it started out as an int or a str, ends up
        encoded the same way in the body — as its text form's bytes with a
        one-byte length prefix — so normalize to a string first.
    Hint 2: Build the entry bytes into a bytearray by looping over items,
        encoding each with str(it).encode('utf-8'), appending its length as
        a single byte, then its raw bytes; only after that body is complete
        do you know the total length to put in the header.
    Hint 3: The 4-byte total-length header field counts the ENTIRE output
        (6-byte header included, not just the body), and it must be written
        big-endian; the entry count in the next 2 bytes is the number of
        items, not the number of body bytes — mixing those two up is the
        easiest way to fail the round-trip check in the tests.
"""

from __future__ import annotations


def rdb_snapshot_ziplist(items: list[str | int]) -> bytes:
    """Encode items into simulated ziplist format:
    - 4 bytes: total bytes
    - 2 bytes: number of entries
    - entries: each entry has 1 byte length + data bytes
    Returns encoded bytes.
    """
    raise NotImplementedError("Implement rdb_snapshot_ziplist")
