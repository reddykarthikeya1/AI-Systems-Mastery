"""Reference solution — Problem 02: Bloom Filter: No False Negatives

Pattern:    Bloom filter
Complexity: Time O((n + q) * hashes), Space O(bits)
"""

from __future__ import annotations


def bloom_check(items: list[str], queries: list[str], bits: int = 8192, hashes: int = 3) -> list[bool]:
    import hashlib

    if bits < 1 or hashes < 1:
        raise ValueError("bits and hashes must both be positive")

    bitset = bytearray(bits)

    def positions(item: str) -> list[int]:
        # hashlib, not hash(): Python's built-in hash is salted per process,
        # so a hash()-based filter gives different answers on every run.
        out = []
        for k in range(hashes):
            digest = hashlib.md5(f"{k}:{item}".encode()).digest()
            out.append(int.from_bytes(digest[:8], "big") % bits)
        return out

    for item in items:
        for p in positions(item):
            bitset[p] = 1

    # True only if EVERY bit is set. This is what forbids false negatives.
    return [all(bitset[p] for p in positions(q)) for q in queries]
