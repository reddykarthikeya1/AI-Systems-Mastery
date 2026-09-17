"""Reference Solution — Problem 01: Redis Crc16 Hash Slot

Topic: 13 Redis Sentinel Clustering Lua
"""

from __future__ import annotations


def redis_crc16_hash_slot(key: str) -> int:
    s = key.find('{')
    if s != -1:
        e = key.find('}', s + 1)
        if e != -1 and e > s + 1:
            key = key[s + 1:e]
    crc = 0
    for byte in key.encode('utf-8'):
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc % 16384
