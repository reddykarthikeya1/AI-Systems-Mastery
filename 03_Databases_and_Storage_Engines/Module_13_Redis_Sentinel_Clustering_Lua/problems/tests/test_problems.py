"""Tests for Redis Crc16 Hash Slot."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_redis_crc16_hash_slot import redis_crc16_hash_slot
except ImportError:
    from p01_redis_crc16_hash_slot import redis_crc16_hash_slot


def test_redis_crc16_hash_slot():
    slot1 = redis_crc16_hash_slot("user:100:profile")
    slot2 = redis_crc16_hash_slot("{user:100}:orders")
    slot3 = redis_crc16_hash_slot("{user:100}:profile")
    assert 0 <= slot1 < 16384
    # Hash tags should guarantee exact same slot
    assert slot2 == slot3
