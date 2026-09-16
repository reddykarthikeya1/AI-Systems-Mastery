"""Property and performance assertions for Probabilistic Data Structures.

These complement the correctness tests in `test_probabilistic_structures.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

import sys

import pytest
from probabilistic_structures import BloomFilter, CountMinSketch, HyperLogLog


def test_bloom_filter_has_no_false_negatives() -> None:
    """The defining asymmetry: 'absent' is always the truth, 'present' may lie.

    This is what makes a Bloom filter safe as a pre-filter - a miss needs no
    confirmation. If this ever fails the structure is unusable, not merely
    inaccurate.
    """
    bloom = BloomFilter(expected_items=5000, fp_rate=0.01)
    added = [f"item:{i}" for i in range(5000)]
    for item in added:
        bloom.add(item)
    for item in added:
        assert item in bloom, f"false negative on {item!r} - impossible by construction"


@pytest.mark.perf
def test_bloom_false_positive_rate_lands_near_the_configured_target() -> None:
    """Sizing is a formula, not a hope. Measure the delivered error rate."""
    target = 0.01
    bloom = BloomFilter(expected_items=5000, fp_rate=target)
    for i in range(5000):
        bloom.add(f"present:{i}")

    probes = 20_000
    false_positives = sum(1 for i in range(probes) if f"absent:{i}" in bloom)
    observed = false_positives / probes

    assert observed <= target * 3, (
        f"observed FP rate {observed:.4f} against a {target:.4f} target - "
        "the bit-array sizing or hash count is wrong."
    )


@pytest.mark.perf
def test_bloom_filter_is_far_smaller_than_the_equivalent_set() -> None:
    """The entire reason to accept false positives is the space saving."""
    n = 20_000
    bloom = BloomFilter(expected_items=n, fp_rate=0.01)
    exact = set()
    for i in range(n):
        key = f"item:{i}"
        bloom.add(key)
        exact.add(key)

    bloom_bytes = sys.getsizeof(bloom.bits) if hasattr(bloom, "bits") else sys.getsizeof(bloom)
    exact_bytes = sys.getsizeof(exact) + sum(sys.getsizeof(k) for k in exact)

    assert bloom_bytes < exact_bytes / 5, (
        f"bloom {bloom_bytes} B vs set {exact_bytes} B - the space win is the point."
    )


def test_count_min_sketch_never_underestimates() -> None:
    """CMS overestimates on collision but must never report fewer than the truth."""
    sketch = CountMinSketch(width=2000, depth=5)
    truth: dict[str, int] = {}
    for i in range(3000):
        key = f"k{i % 400}"
        sketch.increment(key)
        truth[key] = truth.get(key, 0) + 1

    for key, real in truth.items():
        assert sketch.estimate(key) >= real, (
            f"{key}: estimate {sketch.estimate(key)} < actual {real} - "
            "underestimation breaks every guarantee CMS offers."
        )


@pytest.mark.perf
def test_hyperloglog_cardinality_is_within_its_error_bound() -> None:
    """HLL trades exactness for ~1.5 KB regardless of cardinality."""
    hll = HyperLogLog(precision=14)
    true_count = 50_000
    for i in range(true_count):
        hll.add(f"visitor:{i}")

    estimate = hll.count()
    error = abs(estimate - true_count) / true_count
    assert error < 0.05, (
        f"estimated {estimate:,} against {true_count:,} ({error:.2%} error) - "
        "precision 14 should hold well under 5%."
    )


def test_hyperloglog_is_insensitive_to_duplicates() -> None:
    """Counting *distinct* items means re-adding must not move the estimate."""
    hll = HyperLogLog(precision=14)
    for i in range(10_000):
        hll.add(f"u{i}")
    first = hll.count()
    for _ in range(5):
        for i in range(10_000):
            hll.add(f"u{i}")
    assert abs(hll.count() - first) / max(first, 1) < 0.01
