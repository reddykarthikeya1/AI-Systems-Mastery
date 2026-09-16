"""Problem-bank suite for Module_12_Greedy_Algorithms_and_Interval_Scheduling.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_max_profit_stock import max_profit_stock
from p02_merge_intervals import merge_intervals
from p03_max_non_overlapping import max_non_overlapping
from p04_min_arrows import min_arrows
from p05_can_jump import can_jump
from p06_min_jumps import min_jumps
from p07_gas_station import gas_station
from p08_partition_labels import partition_labels


def test_p01_max_profit_stock():
    """Best Time To Buy And Sell Stock — Greedy running minimum (Easy)."""
    assert max_profit_stock([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit_stock([7, 6, 4, 3, 1]) == 0
    assert max_profit_stock([]) == 0
    assert max_profit_stock([5]) == 0
    # Buying and selling the same day is not a trade.
    assert max_profit_stock([3, 3]) == 0
    assert max_profit_stock([1, 2]) == 1
    # The minimum must come strictly before the maximum.
    assert max_profit_stock([9, 1]) == 0
    assert max_profit_stock([2, 4, 1]) == 2
    # Cross-check against brute force.
    for data in ([7, 1, 5, 3, 6, 4], [2, 4, 1], [1, 2, 3, 4], [4, 3, 2, 1], [3, 2, 6, 5, 0, 3]):
        brute = max(
            (data[j] - data[i] for i in range(len(data)) for j in range(i + 1, len(data))),
            default=0,
        )
        assert max_profit_stock(data) == max(brute, 0), data
    # O(n).
    assert max_profit_stock(list(range(100_000))) == 99_999

def test_p02_merge_intervals():
    """Merge Overlapping Intervals — Sort by START, then sweep (Medium)."""
    assert merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]) == [(1, 6), (8, 10), (15, 18)]
    # Touching intervals merge.
    assert merge_intervals([(1, 4), (4, 5)]) == [(1, 5)]
    assert merge_intervals([]) == []
    assert merge_intervals([(1, 5)]) == [(1, 5)]
    # A fully nested interval must not shrink the result.
    assert merge_intervals([(1, 10), (2, 3)]) == [(1, 10)]
    assert merge_intervals([(1, 4), (2, 3)]) == [(1, 4)]
    # Input order must not matter.
    assert merge_intervals([(15, 18), (1, 3), (8, 10), (2, 6)]) == [(1, 6), (8, 10), (15, 18)]
    # No overlaps at all.
    assert merge_intervals([(1, 2), (3, 4)]) == [(1, 2), (3, 4)]
    # Everything collapses to one.
    assert merge_intervals([(1, 100), (2, 3), (4, 5), (50, 60)]) == [(1, 100)]
    # Identical intervals.
    assert merge_intervals([(1, 2), (1, 2)]) == [(1, 2)]
    # The output must be disjoint and sorted.
    data = [(5, 7), (1, 4), (3, 3), (9, 12), (11, 20), (0, 0)]
    got = merge_intervals(data)
    assert got == sorted(got)
    assert all(a[1] < b[0] for a, b in zip(got, got[1:]))

def test_p03_max_non_overlapping():
    """Maximum Non-Overlapping Intervals — Sort by END, then greedy (Medium)."""
    assert max_non_overlapping([(1, 3), (2, 4), (3, 5)]) == 2
    assert max_non_overlapping([]) == 0
    assert max_non_overlapping([(1, 2)]) == 1
    # Touching intervals are both selectable.
    assert max_non_overlapping([(1, 2), (2, 3), (3, 4)]) == 3
    # All identical: only one can be taken.
    assert max_non_overlapping([(1, 5), (1, 5), (1, 5)]) == 1
    # THE case sorting by start gets wrong: start-order takes (1,10), # first and then only 1 fits, giving 1 instead of 3.
    assert max_non_overlapping([(1, 10), (2, 3), (4, 5), (6, 7)]) == 3
    # Nested intervals: take the innermost.
    assert max_non_overlapping([(1, 100), (2, 3)]) == 1
    # Disjoint intervals: take them all.
    assert max_non_overlapping([(1, 2), (3, 4), (5, 6)]) == 3
    # Cross-check against exhaustive subset search.
    import itertools
    for data in (
        [(1, 3), (2, 4), (3, 5)],
        [(1, 10), (2, 3), (4, 5), (6, 7)],
        [(0, 2), (1, 4), (3, 5), (4, 6)],
        [(1, 2), (2, 3)],
    ):
        best = 0
        for r in range(len(data) + 1):
            for combo in itertools.combinations(sorted(data, key=lambda iv: iv[1]), r):
                if all(a[1] <= b[0] for a, b in zip(combo, combo[1:])):
                    best = max(best, r)
        assert max_non_overlapping(data) == best, data

def test_p04_min_arrows():
    """Minimum Arrows To Burst Balloons — Sort by END, then greedy (Medium)."""
    assert min_arrows([(10, 16), (2, 8), (1, 6), (7, 12)]) == 2
    assert min_arrows([(1, 2), (3, 4), (5, 6), (7, 8)]) == 4
    assert min_arrows([(1, 2), (2, 3), (3, 4), (4, 5)]) == 2
    assert min_arrows([]) == 0
    assert min_arrows([(1, 2)]) == 1
    # Identical balloons need one arrow.
    assert min_arrows([(1, 5), (1, 5)]) == 1
    # Fully nested: one arrow at the innermost end.
    assert min_arrows([(1, 100), (2, 3), (2, 3)]) == 1
    # Touching at a point counts as overlapping.
    assert min_arrows([(1, 2), (2, 3)]) == 1
    # Fully disjoint.
    assert min_arrows([(1, 2), (10, 20), (30, 40)]) == 3

def test_p05_can_jump():
    """Jump Game — Greedy reachability (Medium)."""
    assert can_jump([2, 3, 1, 1, 4]) is True
    assert can_jump([3, 2, 1, 0, 4]) is False
    # A single element is already the destination.
    assert can_jump([0]) is True
    assert can_jump([1]) is True
    # A zero at the start blocks everything.
    assert can_jump([0, 1]) is False
    # A zero at the END is fine - you only need to arrive.
    assert can_jump([1, 0]) is True
    assert can_jump([2, 0, 0]) is True
    # One big jump clears everything.
    assert can_jump([5, 0, 0, 0, 0, 0]) is True
    # Cross-check against BFS reachability.
    from collections import deque
    def brute(a):
        seen = {0}
        q = deque([0])
        while q:
            i = q.popleft()
            if i == len(a) - 1:
                return True
            for j in range(i + 1, min(len(a), i + a[i] + 1)):
                if j not in seen:
                    seen.add(j)
                    q.append(j)
        return len(a) == 1
    for data in ([2, 3, 1, 1, 4], [3, 2, 1, 0, 4], [1, 1, 1, 0], [2, 0, 1, 0, 1], [0], [1, 0]):
        assert can_jump(data) is brute(data), data

def test_p06_min_jumps():
    """Jump Game II (Fewest Jumps) — Greedy BFS by levels (Hard)."""
    assert min_jumps([2, 3, 1, 1, 4]) == 2
    assert min_jumps([2, 3, 0, 1, 4]) == 2
    # Already at the destination.
    assert min_jumps([0]) == 0
    assert min_jumps([1]) == 0
    # One jump.
    assert min_jumps([1, 1]) == 1
    assert min_jumps([5, 0, 0, 0, 0, 0]) == 1
    # All ones: one jump per step.
    assert min_jumps([1, 1, 1, 1]) == 3
    # Cross-check against BFS.
    from collections import deque
    def brute(a):
        if len(a) == 1:
            return 0
        seen = {0}
        q = deque([(0, 0)])
        while q:
            i, d = q.popleft()
            for j in range(i + 1, min(len(a), i + a[i] + 1)):
                if j == len(a) - 1:
                    return d + 1
                if j not in seen:
                    seen.add(j)
                    q.append((j, d + 1))
        return -1
    for data in ([2, 3, 1, 1, 4], [1, 1, 1, 1], [2, 1], [3, 1, 1, 1, 1], [1, 2, 3]):
        assert min_jumps(data) == brute(data), data

def test_p07_gas_station():
    """Gas Station Circuit — Greedy with a restart point (Medium)."""
    assert gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert gas_station([2, 3, 4], [3, 4, 3]) == -1
    # A single station with just enough fuel.
    assert gas_station([5], [4]) == 0
    assert gas_station([3], [4]) == -1
    # Exactly balanced.
    assert gas_station([1, 1], [1, 1]) == 0
    with pytest.raises(ValueError):
        gas_station([1], [1, 2])
    # Cross-check against simulating every start.
    def brute(g, c):
        n = len(g)
        for s in range(n):
            tank = 0
            for k in range(n):
                i = (s + k) % n
                tank += g[i] - c[i]
                if tank < 0:
                    break
            else:
                return s
        return -1
    cases = [
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]),
        ([2, 3, 4], [3, 4, 3]),
        ([3, 1, 1], [1, 2, 2]),
        ([5, 1, 2, 3, 4], [4, 4, 1, 5, 1]),
        ([4], [5]),
    ]
    for g, c in cases:
        assert gas_station(g, c) == brute(g, c), (g, c)

def test_p08_partition_labels():
    """Partition Labels — Greedy with last-occurrence bounds (Medium)."""
    assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]
    assert partition_labels("eccbbbbdec") == [10]
    assert partition_labels("a") == [1]
    # All distinct letters split into singletons.
    assert partition_labels("abcdef") == [1, 1, 1, 1, 1, 1]
    # All the same letter is one part.
    assert partition_labels("aaaa") == [4]
    assert partition_labels("abab") == [4]
    assert partition_labels("aabb") == [2, 2]
    # The sizes must sum to the string length, and each letter must, # appear in exactly one part.
    for text in ("ababcbacadefegdehijhklij", "eccbbbbdec", "abac", "xyzzyx", "qwerty"):
        sizes = partition_labels(text)
        assert sum(sizes) == len(text), text
        cursor = 0
        seen_parts = []
        for size in sizes:
            seen_parts.append(set(text[cursor : cursor + size]))
            cursor += size
        for i, a in enumerate(seen_parts):
            for b in seen_parts[i + 1 :]:
                assert not (a & b), (text, a, b)
