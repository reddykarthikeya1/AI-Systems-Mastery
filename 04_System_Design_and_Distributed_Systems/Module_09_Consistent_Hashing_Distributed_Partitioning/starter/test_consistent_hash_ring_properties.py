"""Property and performance assertions for Consistent Hashing & Ring Partitioning.

These complement the correctness tests in `test_consistent_hash_ring.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

import time

import pytest
from consistent_hash_ring import ConsistentHashRing

KEYS = [f"user:{i}" for i in range(4000)]


def _assignments(ring: ConsistentHashRing) -> dict[str, str]:
    return {k: ring.get_node(k) for k in KEYS}


@pytest.mark.perf
def test_adding_a_node_remaps_about_one_over_n_of_keys() -> None:
    """The whole point of consistent hashing, stated as a measurement.

    Naive `hash(key) % N` remaps ~(N-1)/N of all keys when N changes - for 3 to
    4 nodes that is ~75%. A consistent hash ring should move ~1/4, because only
    the keys falling in the new node's arcs are affected.

    If this test fails high, the ring is behaving like modulo hashing and the
    module's central claim is false.
    """
    ring = ConsistentHashRing(["a", "b", "c"], vnodes=150)
    before = _assignments(ring)

    ring.add_node("d")
    after = _assignments(ring)

    moved = sum(1 for k in KEYS if before[k] != after[k])
    fraction = moved / len(KEYS)

    # Ideal is 1/4 = 0.25. Allow generous slack for hash variance, but stay far
    # below the ~0.75 that modulo hashing would produce.
    assert 0.10 <= fraction <= 0.45, (
        f"{fraction:.1%} of keys remapped on a 3->4 node change. "
        "Expected ~25%; modulo hashing would give ~75%."
    )


@pytest.mark.perf
def test_more_vnodes_reduces_distribution_variance() -> None:
    """Virtual nodes exist to fix variance. Measure that they do."""
    few = ConsistentHashRing(["a", "b", "c", "d"], vnodes=1)
    many = ConsistentHashRing(["a", "b", "c", "d"], vnodes=200)

    def spread(ring: ConsistentHashRing) -> float:
        counts: dict[str, int] = {}
        for k in KEYS:
            node = ring.get_node(k)
            counts[node] = counts.get(node, 0) + 1
        ideal = len(KEYS) / 4
        return max(abs(c - ideal) for c in counts.values()) / ideal

    assert spread(many) < spread(few), (
        f"200 vnodes gave spread {spread(many):.2f}, 1 vnode gave {spread(few):.2f}. "
        "More virtual nodes must reduce imbalance, or they serve no purpose."
    )


def test_removing_a_node_never_loses_a_key() -> None:
    """Every key must still resolve to *some* live node after a removal."""
    ring = ConsistentHashRing(["a", "b", "c"], vnodes=100)
    ring.remove_node("b")
    for k in KEYS[:500]:
        node = ring.get_node(k)
        assert node in {"a", "c"}, f"key {k} resolved to {node!r} after removing 'b'"


def test_empty_ring_returns_none_rather_than_raising() -> None:
    """A ring with no nodes is a legitimate transient state during bootstrap."""
    assert ConsistentHashRing([], vnodes=10).get_node("anything") is None


def test_preference_list_is_distinct_and_bounded() -> None:
    """A replica set of 3 that contains the same box twice survives no failure."""
    ring = ConsistentHashRing(["a", "b", "c", "d"], vnodes=120)
    for k in KEYS[:200]:
        prefs = ring.get_preference_list(k, 3)
        assert len(prefs) == len(set(prefs)), f"duplicate physical node in {prefs}"
        assert len(prefs) <= 4


def test_preference_list_larger_than_cluster_is_clamped() -> None:
    ring = ConsistentHashRing(["a", "b"], vnodes=50)
    assert len(ring.get_preference_list("k", 10)) <= 2


@pytest.mark.perf
@pytest.mark.slow
def test_lookup_cost_is_logarithmic_not_linear() -> None:
    """Ring lookup is a binary search over the sorted ring, so growing the ring
    100x must not grow per-lookup cost anywhere near 100x."""

    def per_lookup(n_nodes: int) -> float:
        ring = ConsistentHashRing([f"n{i}" for i in range(n_nodes)], vnodes=50)
        probe = KEYS[:2000]
        start = time.perf_counter()
        for k in probe:
            ring.get_node(k)
        return (time.perf_counter() - start) / len(probe)

    small = per_lookup(3)
    large = per_lookup(300)
    assert large / small < 4.0, (
        f"per-lookup cost grew {large / small:.1f}x when the ring grew 100x - "
        "that is not a binary search."
    )
