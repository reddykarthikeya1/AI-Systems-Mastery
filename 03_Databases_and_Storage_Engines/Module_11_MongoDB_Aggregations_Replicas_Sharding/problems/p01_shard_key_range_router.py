"""Problem 01 — Shard Key Range Router

Topic: 11 MongoDB Aggregations Replicas Sharding
Target: Production-grade implementation

Route query to appropriate shard ID using range-based chunk partitions.

Example:
    >>> chunks = [
    ...     {'min': 0, 'max': 100, 'shard_id': 'shard01'},
    ...     {'min': 100, 'max': 200, 'shard_id': 'shard02'},
    ...     {'min': 200, 'max': 1000, 'shard_id': 'shard03'},
    ... ]
    >>> shard_key_range_router(chunks, 100)
    'shard02'

Hints:
    Hint 1: Each chunk owns a half-open range, so a key value belongs to at
        most one chunk — the boundary value itself always resolves to the
        chunk that starts there, never the one that ends there.
    Hint 2: A simple linear scan over the chunks list checking membership in
        each range is all that's needed; no sorting or binary search is
        required for correctness (only for scale, which is out of scope
        here).
    Hint 3: The range test must be min <= query_key_val < max (inclusive
        lower bound, exclusive upper bound) — query_key_val == 100 above
        must land in shard02, not shard01 — and a key at or past the last
        chunk's max (or matching no chunk at all) must return 'UNROUTED'
        rather than raising or returning None.
"""

from __future__ import annotations


def shard_key_range_router(chunks: list[dict], query_key_val: int) -> str:
    """Each chunk in chunks has: {'min': int, 'max': int, 'shard_id': str}.
    Ranges are [min, max) exclusive of max (or infinity for max chunk).
    Returns shard_id of the matching chunk, or 'UNROUTED' if not found.
    """
    raise NotImplementedError("Implement shard_key_range_router")
