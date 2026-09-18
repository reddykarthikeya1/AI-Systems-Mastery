"""Problem 01 — Redis Crc16 Hash Slot

Topic: 13 Redis Sentinel Clustering Lua
Target: Production-grade implementation

Compute Redis Cluster 16384 hash slot with hash tags support.

Example:
    >>> redis_crc16_hash_slot("{user:100}:orders")
    9308
    >>> redis_crc16_hash_slot("{user:100}:profile")
    9308

Hints:
    Hint 1: The slot must depend only on the "hash tag" portion of a key
        when one is present, so that related keys sharing a tag (like the
        two {user:100} keys above) always land on the same cluster node.
    Hint 2: Locate the substring between the first '{' and the next '}'
        after it; if that substring is non-empty, CRC16 only that substring,
        otherwise CRC16 the whole key — then reduce mod 16384. Implement
        CRC16-CCITT with polynomial 0x1021 over the UTF-8 bytes, bit by bit.
    Hint 3: An empty hash tag like "{}foo" (nothing between the braces) or a
        '{' with no matching '}' must fall back to hashing the entire
        original key, not an empty or partial substring — that edge case is
        exactly what separates a real hash-tag implementation from a naive
        "just slice between the first braces" one.
"""

from __future__ import annotations


def redis_crc16_hash_slot(key: str) -> int:
    """Compute Redis cluster hash slot:
    1. If key contains '{' and '}' with non-empty content between, hash only the content between the first '{' and first '}'.
    2. Otherwise hash entire key.
    3. Return (crc16_val % 16384).
    Use CRC16 polynomial 0x1021.
    """
    raise NotImplementedError("Implement redis_crc16_hash_slot")
