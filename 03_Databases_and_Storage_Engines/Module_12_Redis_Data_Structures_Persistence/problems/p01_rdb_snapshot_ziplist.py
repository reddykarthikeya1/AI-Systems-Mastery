"""Problem 01 — Rdb Snapshot Ziplist

Topic: 12 Redis Data Structures Persistence
Target: Production-grade implementation

Pack list of small integer and string values into compact simulated ziplist byte representation.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
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
