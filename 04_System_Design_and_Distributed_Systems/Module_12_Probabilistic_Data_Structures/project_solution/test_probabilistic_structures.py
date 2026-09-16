"""Unit tests for Probabilistic Data Structures (Bloom Filter, Count-Min, HyperLogLog)."""

from __future__ import annotations

from probabilistic_structures import (
    BloomFilter,
    CountMinSketch,
    HyperLogLog,
)


def test_bloom_filter_zero_false_negatives() -> None:
    bf = BloomFilter(expected_items=1000, fp_rate=0.01)
    added_items = [f"user_{i}" for i in range(1000)]

    for item in added_items:
        bf.add(item)

    # Invariant: Every added item MUST be present (Zero False Negatives)
    for item in added_items:
        assert item in bf


def test_bloom_filter_false_positive_rate_within_bounds() -> None:
    # 5% false positive target
    bf = BloomFilter(expected_items=2000, fp_rate=0.05)
    for i in range(2000):
        bf.add(f"member_{i}")

    # Test 2000 non-members
    false_positives = 0
    test_non_members = 2000
    for i in range(test_non_members):
        if f"non_member_{i}" in bf:
            false_positives += 1

    measured_fp_rate = false_positives / test_non_members
    # Measured FP rate should be close to 0.05 (allowing tolerance up to 0.08)
    assert measured_fp_rate < 0.08


def test_count_min_sketch_never_underestimates() -> None:
    cms = CountMinSketch(width=500, depth=5)

    # Feed item counts
    for _ in range(42):
        cms.increment("apple")
    for _ in range(15):
        cms.increment("banana")

    # Invariant: Estimate must be >= actual count (never underestimates)
    assert cms.estimate("apple") >= 42
    assert cms.estimate("banana") >= 15
    assert cms.estimate("cherry") == 0


def test_hyperloglog_cardinality_estimation_bounds() -> None:
    # Precision 10 -> 1024 registers -> standard error ~ 1.04 / sqrt(1024) = 3.25%
    hll = HyperLogLog(precision=10)
    distinct_count = 5000

    for i in range(distinct_count):
        hll.add(f"unique_visitor_ip_{i}")
        # Add some duplicates to ensure uniqueness is measured
        if i % 3 == 0:
            hll.add(f"unique_visitor_ip_{i}")

    estimated = hll.count()
    error = abs(estimated - distinct_count) / distinct_count

    # Estimated cardinality should be within 10% of true cardinality (well within 3-sigma of 3.25%)
    assert error < 0.10
