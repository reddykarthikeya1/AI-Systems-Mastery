"""Tests for the Fenwick tree and the treap.

Both are checked against the obvious slow implementation on randomised
operation sequences. For a Fenwick tree that is a plain list and `sum()`; for a
treap it is a sorted Python list. Any divergence in a few thousand random
operations is found immediately.
"""

from __future__ import annotations

import random
import time

import pytest
from fenwick_and_treap import (
    FenwickTree,
    Treap,
    UnbalancedBST,
    count_inversions,
    merge,
    split,
)

# ---------------------------------------------------------------------------
# Fenwick tree
# ---------------------------------------------------------------------------


def test_prefix_sums_match_a_plain_list():
    random.seed(14)
    for _ in range(200):
        size = random.randint(1, 40)
        plain = [0] * size
        tree = FenwickTree(size)
        for _ in range(60):
            index = random.randrange(size)
            delta = random.randint(-20, 20)
            plain[index] += delta
            tree.add(index, delta)
            count = random.randint(0, size)
            assert tree.prefix_sum(count) == sum(plain[:count])


def test_range_sum_matches_a_plain_list():
    random.seed(141)
    values = [random.randint(-50, 50) for _ in range(60)]
    tree = FenwickTree.from_values(values)
    for _ in range(300):
        start = random.randint(0, len(values))
        stop = random.randint(start, len(values))
        assert tree.range_sum(start, stop) == sum(values[start:stop])


def test_from_values_equals_repeated_adds():
    values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    built = FenwickTree.from_values(values)
    added = FenwickTree(len(values))
    for index, value in enumerate(values):
        added.add(index, value)
    assert built.tree == added.tree


def test_empty_tree():
    tree = FenwickTree(0)
    assert tree.prefix_sum(0) == 0
    assert tree.range_sum(0, 0) == 0


def test_out_of_range_is_rejected():
    tree = FenwickTree(5)
    with pytest.raises(IndexError):
        tree.add(5, 1)
    with pytest.raises(IndexError):
        tree.add(-1, 1)
    with pytest.raises(IndexError):
        tree.prefix_sum(6)
    with pytest.raises(IndexError):
        tree.range_sum(3, 2)
    with pytest.raises(ValueError):
        FenwickTree(-1)


def test_find_kth_acts_as_an_order_statistic():
    # A multiset held as counts: value v present count[v] times.
    counts = [0, 2, 0, 1, 3]          # -> 1,1,3,4,4,4
    tree = FenwickTree(len(counts))
    for index, count in enumerate(counts):
        tree.add(index, count)

    expanded = [value for value, count in enumerate(counts) for _ in range(count)]
    assert expanded == [1, 1, 3, 4, 4, 4]
    for k, expected in enumerate(expanded):
        assert tree.find_kth(k) == expected, f"k={k}"


def test_count_inversions_matches_brute_force():
    random.seed(1414)
    for _ in range(200):
        values = [random.randint(0, 15) for _ in range(random.randint(0, 25))]
        expected = sum(1 for i in range(len(values))
                       for j in range(i + 1, len(values))
                       if values[i] > values[j])
        assert count_inversions(values) == expected


def test_count_inversions_edge_cases():
    assert count_inversions([]) == 0
    assert count_inversions([1]) == 0
    assert count_inversions([1, 2, 3]) == 0
    assert count_inversions([3, 2, 1]) == 3
    assert count_inversions([2, 2, 2]) == 0, "equal values are not inversions"


# ---------------------------------------------------------------------------
# Treap
# ---------------------------------------------------------------------------


def test_treap_behaves_like_a_sorted_set():
    random.seed(15)
    for trial in range(60):
        treap = Treap(seed=trial)
        model: set[int] = set()
        for _ in range(200):
            key = random.randint(0, 40)
            if random.random() < 0.6:
                assert treap.insert(key) == (key not in model)
                model.add(key)
            else:
                assert treap.erase(key) == (key in model)
                model.discard(key)
            assert len(treap) == len(model)
            assert treap.to_list() == sorted(model)


def test_treap_membership():
    treap = Treap(seed=1)
    for key in (5, 3, 8, 1):
        treap.insert(key)
    assert 5 in treap
    assert 3 in treap
    assert 4 not in treap
    assert not treap.insert(5), "duplicates are rejected"
    assert len(treap) == 4


def test_treap_kth_and_rank():
    treap = Treap(seed=2)
    for key in (50, 10, 40, 20, 30):
        treap.insert(key)
    assert [treap.kth(k) for k in range(5)] == [10, 20, 30, 40, 50]
    assert treap.rank(10) == 0
    assert treap.rank(35) == 3
    assert treap.rank(50) == 4
    assert treap.rank(99) == 5
    with pytest.raises(IndexError):
        treap.kth(5)
    with pytest.raises(IndexError):
        treap.kth(-1)


def test_treap_erase_missing_key_is_a_no_op():
    treap = Treap(seed=3)
    treap.insert(1)
    assert not treap.erase(99)
    assert treap.to_list() == [1]


def test_split_and_merge_round_trip():
    random.seed(151)
    treap = Treap(seed=4)
    for key in random.sample(range(100), 40):
        treap.insert(key)
    original = treap.to_list()

    low, high = split(treap.root, 50)
    lows, highs = Treap(), Treap()
    lows.root, highs.root = low, high
    assert lows.to_list() == [k for k in original if k < 50]
    assert highs.to_list() == [k for k in original if k >= 50]

    treap.root = merge(low, high)
    assert treap.to_list() == original, "merge must restore exactly what split cut"


def test_subtree_sizes_stay_consistent():
    """If `size` drifts, `kth` returns the wrong element silently."""
    random.seed(152)
    treap = Treap(seed=5)
    keys = random.sample(range(500), 200)
    for key in keys:
        treap.insert(key)
    for key in keys[:80]:
        treap.erase(key)

    expected = sorted(set(keys) - set(keys[:80]))
    assert len(treap) == len(expected)
    assert [treap.kth(k) for k in range(len(expected))] == expected


# ---------------------------------------------------------------------------
# the point of randomised balancing
# ---------------------------------------------------------------------------


def test_treap_stays_shallow_on_sorted_input():
    """Sorted insertion is the worst case for a plain BST and a non-case for a
    treap, because the shape follows the random priorities, not the input order.
    """
    n = 4_000
    treap = Treap(seed=6)
    for key in range(n):
        treap.insert(key)

    plain = UnbalancedBST()
    for key in range(n):
        plain.insert(key)

    assert plain.height() == n, "a plain BST degenerates into a linked list"
    assert treap.height() < 4 * (n.bit_length()), (
        f"treap height {treap.height()} should be around 2*log2({n}) "
        f"= {2 * n.bit_length()}")


@pytest.mark.perf
def test_fenwick_beats_recomputing_prefix_sums():
    """The comparison that justifies the structure: 20,000 interleaved updates
    and queries against a list that must re-sum on every query.
    """
    size, operations = 20_000, 20_000
    random.seed(153)
    indices = [random.randrange(size) for _ in range(operations)]

    plain = [0] * size
    start = time.perf_counter()
    for i, index in enumerate(indices):
        plain[index] += 1
        if i % 2:
            sum(plain[:index])
    naive_seconds = time.perf_counter() - start

    tree = FenwickTree(size)
    start = time.perf_counter()
    for i, index in enumerate(indices):
        tree.add(index, 1)
        if i % 2:
            tree.prefix_sum(index)
    fenwick_seconds = time.perf_counter() - start

    assert fenwick_seconds < naive_seconds / 10, (
        f"Fenwick {fenwick_seconds * 1000:.1f} ms vs "
        f"list {naive_seconds * 1000:.1f} ms")
