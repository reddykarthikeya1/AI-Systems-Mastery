#!/usr/bin/env python3
"""Module 12 Demo: Exact Memory vs. Probabilistic Data Structures Benchmark."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from probabilistic_structures import (
    BloomFilter,
    CountMinSketch,
    HyperLogLog,
)


def main() -> None:
    print("=" * 72)
    print("  MODULE 12: PROBABILISTIC DATA STRUCTURES BENCHMARK")
    print("=" * 72)

    n_items = 50_000
    print(f"\nSimulating stream of {n_items:,} unique visitor identifiers...")

    # 1. Exact Python Set vs Bloom Filter
    exact_set = set()
    bloom = BloomFilter(expected_items=n_items, fp_rate=0.01)

    for i in range(n_items):
        item = f"user-session-token-{i}"
        exact_set.add(item)
        bloom.add(item)

    exact_memory_bytes = sys.getsizeof(exact_set)
    bloom_memory_bytes = sys.getsizeof(bloom.bit_array)

    print("\n--- 1. Set Membership: Exact Hash Set vs Bloom Filter ---")
    print(f"  Exact Python Set Memory: {exact_memory_bytes / 1024 / 1024:8.2f} MB")
    print(f"  Bloom Filter Memory:     {bloom_memory_bytes / 1024:8.2f} KB")
    print(f"  Memory Savings Ratio:    {exact_memory_bytes / bloom_memory_bytes:8.1f}x smaller!")
    print(f"  Bloom Filter Bit Count:  {bloom.num_bits:,} bits ({bloom.num_hashes} hash functions)")

    # 2. HyperLogLog Cardinality Estimation
    print("\n--- 2. Unique Cardinality: Exact Count vs HyperLogLog ---")
    hll = HyperLogLog(precision=11)  # 2048 registers
    for i in range(n_items):
        hll.add(f"visitor-{i}")
        if i % 2 == 0:
            hll.add(f"visitor-{i}")  # duplicate hits

    estimated_unique = hll.count()
    error_pct = abs(estimated_unique - n_items) / n_items * 100.0
    hll_memory_bytes = sys.getsizeof(hll.registers)

    print(f"  Exact Unique Count:      {n_items:,}")
    print(f"  HLL Estimated Count:     {estimated_unique:,} (Error: {error_pct:.2f}%)")
    print(f"  HLL Register Memory:     {hll_memory_bytes / 1024:.2f} KB (Fixed size forever!)")

    # 3. Count-Min Sketch Frequency
    print("\n--- 3. Frequency Estimation: Count-Min Sketch ---")
    cms = CountMinSketch(width=1000, depth=5)
    cms.increment("page:/pricing", 14_820)
    cms.increment("page:/checkout", 3_210)

    print(f"  Estimated '/pricing'  views: {cms.estimate('page:/pricing'):,} (True: 14,820)")
    print(f"  Estimated '/checkout' views: {cms.estimate('page:/checkout'):,} (True: 3,210)")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
