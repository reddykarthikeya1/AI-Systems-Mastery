#!/usr/bin/env python3
"""Module 12: In-Process Architectural Simulation Model: Probabilistic Data Structures.

Implements:
1. Scalable Bloom Filter (Double hashing, zero false negatives)
2. Count-Min Sketch (Sublinear frequency estimation)
3. HyperLogLog (Logarithmic cardinality estimation)
"""

from __future__ import annotations

import hashlib
import math
from typing import Any

# ============================================================================
# 1. Bloom Filter (Kirsch-Mitzenmacher Double Hashing)
# ============================================================================


class BloomFilter:
    """Space-efficient probabilistic set membership filter.

    Guarantees ZERO False Negatives:
    - If `contains(item)` is False -> item is 100% definitely NOT in set.
    - If `contains(item)` is True  -> item is PROBABLY in set (within error rate `fp_rate`).
    """

    def __init__(self, expected_items: int = 10_000, fp_rate: float = 0.01) -> None:
        if expected_items <= 0:
            raise ValueError("expected_items must be positive")
        if not (0 < fp_rate < 1):
            raise ValueError("fp_rate must be between 0 and 1")

        self.expected_items = expected_items
        self.fp_rate = fp_rate

        # Optimal bit array size m = - (n * ln(p)) / (ln(2)^2)
        self.num_bits = math.ceil(-(expected_items * math.log(fp_rate)) / (math.log(2) ** 2))
        # Optimal hash functions count k = (m / n) * ln(2)
        self.num_hashes = math.ceil((self.num_bits / expected_items) * math.log(2))

        # Bit array implemented as list of booleans
        self.bit_array = [False] * self.num_bits
        self.count = 0

    def _hashes(self, item: str) -> list[int]:
        """Kirsch-Mitzenmacher optimization: generates k hash values using 2 hash digests."""
        h1 = int(hashlib.md5(item.encode("utf-8")).hexdigest(), 16)
        h2 = int(hashlib.sha1(item.encode("utf-8")).hexdigest(), 16)

        return [(h1 + i * h2) % self.num_bits for i in range(self.num_hashes)]

    def add(self, item: str) -> None:
        for bit_index in self._hashes(item):
            self.bit_array[bit_index] = True
        self.count += 1

    def __contains__(self, item: str) -> bool:
        return all(self.bit_array[bit_index] for bit_index in self._hashes(item))


# ============================================================================
# 2. Count-Min Sketch (Streaming Frequency Estimation)
# ============================================================================


class CountMinSketch:
    """Probabilistic frequency estimation table with sublinear memory bounds."""

    def __init__(self, width: int = 1000, depth: int = 5) -> None:
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]

    def _hash(self, item: str, row: int) -> int:
        digest = hashlib.md5(f"{row}:{item}".encode()).hexdigest()
        return int(digest, 16) % self.width

    def increment(self, item: str, amount: int = 1) -> None:
        for row in range(self.depth):
            col = self._hash(item, row)
            self.table[row][col] += amount

    def estimate(self, item: str) -> int:
        """Returns frequency estimate. Never underestimates, but may overestimate due to collisions."""
        return min(self.table[row][self._hash(item, row)] for row in range(self.depth))


# ============================================================================
# 3. HyperLogLog (Cardinality Estimation)
# ============================================================================


class HyperLogLog:
    """HyperLogLog cardinality estimator using trailing zero bit analysis.

    Standard error is ~ 1.04 / sqrt(2^p).
    """

    def __init__(self, precision: int = 10) -> None:
        if not (4 <= precision <= 16):
            raise ValueError("Precision p must be between 4 and 16")
        self.p = precision
        self.m = 1 << precision  # Number of registers (2^p)
        self.registers = [0] * self.m

        # Alpha constant for bias correction
        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1.0 + 1.079 / self.m)

    def _rho(self, w: int) -> int:
        """Returns position of leftmost 1-bit (1-indexed)."""
        if w == 0:
            return 32
        return (w & -w).bit_length()

    def add(self, item: Any) -> None:
        # 32-bit hash
        x = int(hashlib.sha256(str(item).encode("utf-8")).hexdigest()[:8], 16)
        # Register index j = first p bits
        j = x >> (32 - self.p)
        # Remaining bits w
        w = x & ((1 << (32 - self.p)) - 1)
        self.registers[j] = max(self.registers[j], self._rho(w))

    def count(self) -> int:
        """Estimates number of distinct items added."""
        # Harmonic mean of 2^register
        harmonic_sum = sum(2.0 ** (-reg) for reg in self.registers)
        raw_estimate = self.alpha * (self.m**2) / harmonic_sum

        # Small range correction (Linear Counting for sparse registers)
        if raw_estimate <= 2.5 * self.m:
            zeros = self.registers.count(0)
            if zeros != 0:
                return round(self.m * math.log(self.m / zeros))

        return round(raw_estimate)
