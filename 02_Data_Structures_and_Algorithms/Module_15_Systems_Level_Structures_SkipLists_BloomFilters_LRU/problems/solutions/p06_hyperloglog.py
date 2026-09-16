"""Reference solution — Problem 06: Approximate Distinct Count

Pattern:    Probabilistic cardinality estimation
Complexity: Time O(n), Space O(registers)
"""

from __future__ import annotations


def approx_distinct(items: list[str], registers: int = 1024) -> int:
    import hashlib

    if registers < 16 or (registers & (registers - 1)) != 0:
        raise ValueError("registers must be a power of two and at least 16")

    m = registers
    bucket_bits = m.bit_length() - 1
    buckets = [0] * m

    for item in items:
        # hashlib for reproducibility: hash() is salted per process.
        h = int.from_bytes(hashlib.sha1(item.encode()).digest()[:8], "big")
        idx = h & (m - 1)                       # which register
        rest = h >> bucket_bits
        # Position of the first 1 bit in the remainder, 1-based.
        rank = 1
        while rest & 1 == 0 and rank <= 64:
            rank += 1
            rest >>= 1
        if rank > buckets[idx]:
            buckets[idx] = rank

    # Standard alpha constants for the bias correction.
    if m == 16:
        alpha = 0.673
    elif m == 32:
        alpha = 0.697
    elif m == 64:
        alpha = 0.709
    else:
        alpha = 0.7213 / (1 + 1.079 / m)

    harmonic = sum(2.0 ** -b for b in buckets)
    estimate = alpha * m * m / harmonic

    # Small-range correction: with empty registers, linear counting is far more
    # accurate than the raw estimator.
    zeros = buckets.count(0)
    if estimate <= 2.5 * m and zeros:
        import math

        estimate = m * math.log(m / zeros)

    return round(estimate)
