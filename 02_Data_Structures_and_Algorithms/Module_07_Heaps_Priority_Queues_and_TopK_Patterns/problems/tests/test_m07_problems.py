"""Problem-bank suite for Module_07_Heaps_Priority_Queues_and_TopK_Patterns.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_kth_largest import kth_largest
from p02_merge_k_sorted import merge_k_sorted
from p03_streaming_median import streaming_median
from p04_k_closest_points import k_closest_points
from p05_last_stone_weight import last_stone_weight
from p06_min_meeting_rooms import min_meeting_rooms
from p07_task_scheduler import task_scheduler
from p08_reorganize_string import reorganize_string


def test_p01_kth_largest():
    """K-th Largest Element — Min-heap of size k (Medium)."""
    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert kth_largest([1], 1) == 1
    # k = 1 is the maximum, k = n is the minimum.
    assert kth_largest([7, 3, 9, 1], 1) == 9
    assert kth_largest([7, 3, 9, 1], 4) == 1
    # Duplicates occupy distinct positions.
    assert kth_largest([5, 5, 5], 2) == 5
    assert kth_largest([2, 2, 1], 2) == 2
    # Negative values.
    assert kth_largest([-1, -5, -3], 2) == -3
    with pytest.raises(ValueError):
        kth_largest([1, 2], 3)
    with pytest.raises(ValueError):
        kth_largest([1, 2], 0)
    # Cross-check every k against a sort.
    data = [9, 4, 7, 1, 7, 3, 8, 2]
    ordered = sorted(data, reverse=True)
    for k in range(1, len(data) + 1):
        assert kth_largest(data, k) == ordered[k - 1], k
    # Scale.
    big = list(range(100_000))
    assert kth_largest(big, 3) == 99_997

def test_p02_merge_k_sorted():
    """Merge K Sorted Lists — Min-heap k-way merge (Hard)."""
    assert merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert merge_k_sorted([]) == []
    assert merge_k_sorted([[]]) == []
    assert merge_k_sorted([[], []]) == []
    assert merge_k_sorted([[1]]) == [1]
    # Some lists empty, some not.
    assert merge_k_sorted([[], [1, 2], []]) == [1, 2]
    # Disjoint ranges.
    assert merge_k_sorted([[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 4, 5, 6]
    assert merge_k_sorted([[5, 6], [3, 4], [1, 2]]) == [1, 2, 3, 4, 5, 6]
    # All values identical across lists - the tie-breaking case.
    assert merge_k_sorted([[2, 2], [2], [2, 2]]) == [2] * 5
    # Negative values.
    assert merge_k_sorted([[-3, -1], [-2, 0]]) == [-3, -2, -1, 0]
    # Cross-check against concatenate-and-sort.
    data = [[1, 5, 9], [2, 2, 8], [], [0, 3, 3, 7], [4]]
    assert merge_k_sorted(data) == sorted(x for lst in data for x in lst)
    # Scale: 1000 lists of 100 elements.
    many = [list(range(i, i + 100)) for i in range(1000)]
    merged = merge_k_sorted(many)
    assert len(merged) == 100_000 and merged == sorted(merged)

def test_p03_streaming_median():
    """Median From A Data Stream — Two heaps (Hard)."""
    assert streaming_median([2, 3, 4]) == [2.0, 2.5, 3.0]
    assert streaming_median([1]) == [1.0]
    assert streaming_median([1, 2]) == [1.0, 1.5]
    # Descending input exercises the rebalancing hardest.
    assert streaming_median([5, 4, 3, 2, 1]) == [5.0, 4.5, 4.0, 3.5, 3.0]
    # Duplicates.
    assert streaming_median([2, 2, 2]) == [2.0, 2.0, 2.0]
    # Negatives.
    assert streaming_median([-1, -2, -3]) == [-1.0, -1.5, -2.0]
    # Cross-check against a naive re-sort at every step.
    import statistics
    data = [41, 35, 62, 5, 97, 97, 21, 3, 88, 54, 11]
    expected = [
        float(statistics.median(data[: i + 1])) for i in range(len(data))
    ]
    assert streaming_median(data) == expected
    # Scale: the naive approach would be ~10^10 operations.
    big = list(range(50_000))
    med = streaming_median(big)
    assert len(med) == 50_000
    # Median of 0..49999 is the mean of the two middle values.
    assert med[-1] == (24_999 + 25_000) / 2
    assert med[0] == 0.0

def test_p04_k_closest_points():
    """K Closest Points To The Origin — Max-heap of size k (Medium)."""
    assert k_closest_points([(1, 3), (-2, 2)], 1) == [(-2, 2)]
    assert k_closest_points([(3, 3), (5, -1), (-2, 4)], 2) == [(3, 3), (-2, 4)]
    assert k_closest_points([(0, 0)], 1) == [(0, 0)]
    # k equal to the number of points returns all of them, sorted.
    got = k_closest_points([(2, 0), (1, 0), (3, 0)], 3)
    assert got == [(1, 0), (2, 0), (3, 0)]
    # Equal distances - deterministic tie-break by x then y.
    got = k_closest_points([(0, 1), (1, 0), (-1, 0), (0, -1)], 4)
    assert got == [(-1, 0), (0, -1), (0, 1), (1, 0)]
    with pytest.raises(ValueError):
        k_closest_points([(1, 1)], 2)
    # Cross-check against a full sort.
    pts = [(3, -1), (-2, 5), (0, 2), (4, 4), (-1, -1), (2, 2)]
    expected = sorted(pts, key=lambda p: (p[0] ** 2 + p[1] ** 2, p[0], p[1]))
    for k in range(1, len(pts) + 1):
        assert k_closest_points(pts, k) == expected[:k], k

def test_p05_last_stone_weight():
    """Last Stone Weight — Max-heap simulation (Easy)."""
    assert last_stone_weight([2, 7, 4, 1, 8, 1]) == 1
    assert last_stone_weight([1]) == 1
    # Two equal stones annihilate.
    assert last_stone_weight([3, 3]) == 0
    assert last_stone_weight([2, 2, 2, 2]) == 0
    # An odd stone survives.
    assert last_stone_weight([1, 1, 1]) == 1
    assert last_stone_weight([10, 4]) == 6
    # Pushing a zero back would give 2 here instead of 0.
    assert last_stone_weight([2, 2]) == 0
    # Worked by hand: 40-33=7 -> 31-26=5 -> 21-7=14 -> 14-5=9.
    assert last_stone_weight([31, 26, 33, 21, 40]) == 9

def test_p06_min_meeting_rooms():
    """Minimum Meeting Rooms — Heap of end times (Medium)."""
    assert min_meeting_rooms([(0, 30), (5, 10), (15, 20)]) == 2
    assert min_meeting_rooms([(7, 10), (2, 4)]) == 1
    assert min_meeting_rooms([]) == 0
    assert min_meeting_rooms([(1, 5)]) == 1
    # Touching intervals share a room: ending at t frees it for t.
    assert min_meeting_rooms([(1, 2), (2, 3), (3, 4)]) == 1
    # Fully nested meetings all need their own room.
    assert min_meeting_rooms([(1, 10), (2, 9), (3, 8)]) == 3
    # Identical meetings.
    assert min_meeting_rooms([(1, 5), (1, 5), (1, 5)]) == 3
    # Input order must not matter.
    assert min_meeting_rooms([(15, 20), (0, 30), (5, 10)]) == 2
    # Cross-check against a sweep over all event points.
    data = [(0, 5), (1, 3), (2, 8), (6, 7), (7, 9), (8, 12), (2, 4)]
    points = sorted({t for iv in data for t in iv})
    brute = max(sum(1 for s, e in data if s <= t < e) for t in points)
    assert min_meeting_rooms(data) == brute

def test_p07_task_scheduler():
    """Task Scheduler With Cooldown — Greedy counting (heap-free) (Medium)."""
    assert task_scheduler(["A", "A", "A", "B", "B", "B"], 2) == 8
    assert task_scheduler(["A", "A", "A", "B", "B", "B"], 0) == 6
    assert task_scheduler(["A"], 5) == 1
    # No cooldown means no idling ever.
    assert task_scheduler(["A", "B", "C"], 0) == 3
    # All distinct: the frame never binds.
    assert task_scheduler(["A", "B", "C", "D"], 2) == 4
    # One task repeated with a long cooldown is nearly all idle.
    assert task_scheduler(["A", "A", "A"], 2) == 7
    # Ties at the top frequency.
    assert task_scheduler(["A", "A", "B", "B"], 2) == 5
    assert task_scheduler(["A", "A", "A", "B", "B", "C", "C"], 2) == 7
    # Many distinct tasks: length equals the task count.
    assert task_scheduler(["A","A","A","A","B","C","D","E","F","G"], 2) == 10

def test_p08_reorganize_string():
    """Reorganize String — Greedy with a max-heap (Hard)."""
    assert reorganize_string("aab") == "aba"
    assert reorganize_string("aaab") == ""
    assert reorganize_string("a") == "a"
    assert reorganize_string("aa") == ""
    # Any valid arrangement is acceptable, so check the PROPERTY.
    for text in ("aab", "vvvlo", "abbabbaaab", "aabbcc", "abcabc", "aaabbbccc"):
        got = reorganize_string(text)
        assert sorted(got) == sorted(text), text
        assert all(a != b for a, b in zip(got, got[1:])), (text, got)
    # Impossible cases must return the empty string.
    for text in ("aaab", "aa", "aaaaab"):
        assert reorganize_string(text) == "", text
    # Exactly at the feasibility boundary.
    got = reorganize_string("aabb")
    assert len(got) == 4 and all(a != b for a, b in zip(got, got[1:]))
    got = reorganize_string("aabbb")
    assert len(got) == 5 and all(a != b for a, b in zip(got, got[1:]))
