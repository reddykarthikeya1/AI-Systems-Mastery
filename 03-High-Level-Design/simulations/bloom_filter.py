#!/usr/bin/env python3
"""
===============================================================================
Bloom Filter Simulator & Mathematical Verifier
===============================================================================
Metaphor:
  A VIP nightclub bouncer with a tiny index card.
  - If your name does NOT match the hashes on the card, the bouncer says:
    "You are DEFINITELY NOT on the guest list." (Zero False Negatives)
  - If it matches, the bouncer says:
    "You are PROBABLY on the guest list." (Small False Positive Probability p)

Why High-Level Design Uses This:
  - Cassandra, RocksDB, and Bigtable use Bloom Filters to avoid expensive disk
    seeks for non-existent row keys.
  - Akamai / CDNs use Bloom Filters to avoid caching "one-hit-wonder" web pages.
===============================================================================
"""

import math
import hashlib
from typing import List


class BloomFilter:
    """
    Space-efficient probabilistic data structure.
    Guarantees:
      - False Negatives: NEVER (0%)
      - False Positives: Controlled by m (bits) and k (hash functions)
    """

    def __init__(self, expected_elements: int, false_positive_rate: float):
        if not (0 < false_positive_rate < 1):
            raise ValueError("false_positive_rate must be between 0 and 1.")
        
        self.n = expected_elements
        self.p = false_positive_rate

        # Optimal bit array size: m = - (n * ln(p)) / (ln(2)^2)
        self.m = int(- (self.n * math.log(self.p)) / (math.log(2) ** 2))
        
        # Optimal number of hash functions: k = (m / n) * ln(2)
        self.k = int(round((self.m / self.n) * math.log(2)))

        # Allocate bit array using bytearray (8 bits per byte)
        # Size in bytes = ceil(m / 8)
        self.byte_count = (self.m + 7) // 8
        self.bit_array = bytearray(self.byte_count)

        self.count = 0

    def _hashes(self, item: str) -> List[int]:
        """
        Double-hashing technique (Kirsch-Mitzenmacher):
        hash_i(x) = (hash1(x) + i * hash2(x)) % m
        Produces k distinct hash values using only two 64-bit cryptographic digests.
        """
        # MD5 digest yields 16 bytes = two 64-bit integers
        digest = hashlib.md5(item.encode("utf-8")).digest()
        h1 = int.from_bytes(digest[:8], byteorder="big")
        h2 = int.from_bytes(digest[8:], byteorder="big")

        positions = []
        for i in range(self.k):
            pos = (h1 + i * h2) % self.m
            positions.append(pos)
        return positions

    def add(self, item: str) -> None:
        """Sets the k bits corresponding to the item to 1."""
        for bit_index in self._hashes(item):
            byte_idx = bit_index // 8
            bit_offset = bit_index % 8
            self.bit_array[byte_idx] |= (1 << bit_offset)
        self.count += 1

    def contains(self, item: str) -> bool:
        """
        Returns False if item is DEFINITIVELY NOT in the filter.
        Returns True if item is PROBABLY in the filter.
        """
        for bit_index in self._hashes(item):
            byte_idx = bit_index // 8
            bit_offset = bit_index % 8
            if not (self.bit_array[byte_idx] & (1 << bit_offset)):
                return False
        return True

    def memory_footprint_kb(self) -> float:
        return len(self.bit_array) / 1024.0


def run_experiment():
    print("=" * 70)
    print(" BLOOM FILTER MATHEMATICAL SIMULATION & PRODUCTION BENCHMARK")
    print("=" * 70)

    TARGET_ELEMENTS = 50_000
    TARGET_FPR = 0.01  # 1% False Positive Rate

    bf = BloomFilter(expected_elements=TARGET_ELEMENTS, false_positive_rate=TARGET_FPR)

    print(f"Target Capacity (n)        : {TARGET_ELEMENTS:,} items")
    print(f"Target False Positive Rate : {TARGET_FPR * 100:.2f}%")
    print(f"Calculated Optimal Bits (m): {bf.m:,} bits ({bf.memory_footprint_kb():.2f} KB)")
    print(f"Optimal Hash Functions (k) : {bf.k} hashes per item")
    print(f"Bits per Element Ratio     : {bf.m / TARGET_ELEMENTS:.2f} bits/element")
    print("-" * 70)

    # 1. Insertion
    print(f"[*] Inserting {TARGET_ELEMENTS:,} members (e.g., 'user_id_<x>')...")
    for i in range(TARGET_ELEMENTS):
        bf.add(f"user_id_{i}")

    # 2. Verification of Zero False Negatives
    print("[*] Verifying False Negative Rate on all inserted elements...")
    false_negatives = 0
    for i in range(TARGET_ELEMENTS):
        if not bf.contains(f"user_id_{i}"):
            false_negatives += 1

    print(f"    False Negatives Observed: {false_negatives} / {TARGET_ELEMENTS}")
    assert false_negatives == 0, "[CRITICAL] Bloom Filter violated invariant: False Negative found!"
    print("    [PASS] Bloom Filter Invariant verified: ZERO False Negatives.")

    # 3. False Positive Rate Test on Unseen Elements
    TEST_NON_MEMBERS = 100_000
    print(f"[*] Querying {TEST_NON_MEMBERS:,} UNSEEN elements (e.g., 'stranger_<x>')...")
    false_positives = 0
    for i in range(TEST_NON_MEMBERS):
        if bf.contains(f"stranger_{i}"):
            false_positives += 1

    empirical_fpr = false_positives / TEST_NON_MEMBERS
    print(f"    False Positives Observed : {false_positives:,} / {TEST_NON_MEMBERS:,}")
    print(f"    Empirical FPR            : {empirical_fpr * 100:.3f}% (Expected ~{TARGET_FPR * 100:.2f}%)")

    # 4. Storage Comparison vs Python HashSet
    # A standard Python set of 50,000 strings takes ~4MB
    import sys
    naive_set = {f"user_id_{i}" for i in range(TARGET_ELEMENTS)}
    naive_size_kb = sys.getsizeof(naive_set) / 1024.0

    print("-" * 70)
    print(" PRODUCTION MEMORY EFFICIENCY ANALYSIS:")
    print(f"  - Naive Python Set (In-Memory RAM) : ~{naive_size_kb:,.1f} KB")
    print(f"  - Bloom Filter (Compressed Bits)   : ~{bf.memory_footprint_kb():,.1f} KB")
    print(f"  - Space Savings                    : {(1.0 - (bf.memory_footprint_kb() / naive_size_kb)) * 100:.1f}% reduction!")
    print("=" * 70)


if __name__ == "__main__":
    run_experiment()
