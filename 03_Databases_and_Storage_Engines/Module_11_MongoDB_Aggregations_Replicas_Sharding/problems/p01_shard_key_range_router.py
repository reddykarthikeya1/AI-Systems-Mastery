"""Problem 01 — Shard Key Range Router

Topic: 11 MongoDB Aggregations Replicas Sharding
Target: Production-grade implementation

Route query to appropriate shard ID using range-based chunk partitions.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def shard_key_range_router(chunks: list[dict], query_key_val: int) -> str:
    """Each chunk in chunks has: {'min': int, 'max': int, 'shard_id': str}.
    Ranges are [min, max) exclusive of max (or infinity for max chunk).
    Returns shard_id of the matching chunk, or 'UNROUTED' if not found.
    """
    raise NotImplementedError("Implement shard_key_range_router")
