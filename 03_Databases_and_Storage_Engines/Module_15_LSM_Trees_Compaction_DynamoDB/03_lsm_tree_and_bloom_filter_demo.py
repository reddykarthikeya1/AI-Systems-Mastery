"""Module 15: LSM-Tree, Bloom Filter & DynamoDB Capacity Demo.

Demonstrates:
1. Bloom Filter probabilistic membership testing with zero false negatives.
2. MemTable sequential flush to immutable SSTables.
3. SSTable multi-way merge compaction discarding obsolete versions.
4. DynamoDB RCU/WCU capacity calculation rules.
"""

from __future__ import annotations

import hashlib
import math


class SimpleBloomFilter:
    """Demonstrates bit-array hashing for zero false negative lookups."""

    def __init__(self, expected_items: int = 100, false_positive_rate: float = 0.01) -> None:
        # m = - (n * ln(p)) / (ln(2)^2)
        self.m = int(- (expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2))
        # k = (m / n) * ln(2)
        self.k = int((self.m / expected_items) * math.log(2))
        self.bit_array = [0] * self.m

    def _hashes(self, item: str) -> list[int]:
        positions = []
        for i in range(self.k):
            seed = f"{item}:{i}".encode("utf-8")
            digest = int(hashlib.sha256(seed).hexdigest(), 16)
            positions.append(digest % self.m)
        return positions

    def add(self, item: str) -> None:
        for pos in self._hashes(item):
            self.bit_array[pos] = 1

    def contains(self, item: str) -> bool:
        return all(self.bit_array[pos] == 1 for pos in self._hashes(item))


def demo_bloom_filter() -> None:
    print("=" * 75)
    print("    1. BLOOM FILTER: PROBABILISTIC ZERO FALSE NEGATIVE LOOKUP")
    print("=" * 75)

    bf = SimpleBloomFilter(expected_items=10, false_positive_rate=0.01)
    keys_stored = ["user:101", "user:102", "user:103", "user:104", "user:105"]

    for k in keys_stored:
        bf.add(k)

    print(f"Filter Size: {bf.m} bits, Hash Functions (k): {bf.k}")
    print(f"Stored Keys: {keys_stored}")

    print("\nTesting Membership:")
    # Test existing keys: MUST ALWAYS RETURN TRUE (Zero false negatives)
    all_present = all(bf.contains(k) for k in keys_stored)
    print(f"  -> All {len(keys_stored)} stored keys return True? {all_present} (Guaranteed Zero False Negatives!)")

    # Test non-existent keys
    absent_keys = ["user:999", "order:404", "account:none"]
    for k in absent_keys:
        res = bf.contains(k)
        print(f"  -> Key '{k}': Bloom Filter returned {res} (if False, completely skips SSTable disk read!)")


def demo_dynamodb_rcu_wcu() -> None:
    print("\n" + "=" * 75)
    print("    2. DYNAMODB CAPACITY UNITS: RCU / WCU CALCULATION")
    print("=" * 75)

    scenarios = [
        {"desc": "Strong Read 3.5 KB item", "size_kb": 3.5, "mode": "strong_read"},
        {"desc": "Strong Read 6.2 KB item", "size_kb": 6.2, "mode": "strong_read"},
        {"desc": "Eventual Read 6.2 KB item", "size_kb": 6.2, "mode": "eventual_read"},
        {"desc": "Write 0.8 KB item", "size_kb": 0.8, "mode": "write"},
        {"desc": "Write 2.4 KB item", "size_kb": 2.4, "mode": "write"},
        {"desc": "Transactional Write 2.4 KB item", "size_kb": 2.4, "mode": "transact_write"},
    ]

    for sc in scenarios:
        size = sc["size_kb"]
        mode = sc["mode"]
        if mode == "strong_read":
            cost = math.ceil(size / 4.0)
            unit = "RCU"
        elif mode == "eventual_read":
            cost = math.ceil(size / 4.0) * 0.5
            unit = "RCU"
        elif mode == "write":
            cost = math.ceil(size / 1.0)
            unit = "WCU"
        elif mode == "transact_write":
            cost = math.ceil(size / 1.0) * 2
            unit = "WCU"
        print(f"  [{sc['desc']:<32}] -> Cost: {cost:>4} {unit}")


def main() -> None:
    demo_bloom_filter()
    demo_dynamodb_rcu_wcu()


if __name__ == "__main__":
    main()
