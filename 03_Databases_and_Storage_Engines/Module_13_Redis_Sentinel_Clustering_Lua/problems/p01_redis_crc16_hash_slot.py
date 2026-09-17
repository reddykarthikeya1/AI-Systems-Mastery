"""Problem 01 — Redis Crc16 Hash Slot

Topic: 13 Redis Sentinel Clustering Lua
Target: Production-grade implementation

Compute Redis Cluster 16384 hash slot with hash tags support.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
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
