"""Unit tests for IntervalSchedulingEngine."""
from interval_scheduling_engine import IntervalSchedulingEngine


def test_merge_intervals():
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    assert IntervalSchedulingEngine.merge_intervals(intervals) == [[1, 6], [8, 10], [15, 18]]

    disjoint = [[1, 4], [4, 5]]
    assert IntervalSchedulingEngine.merge_intervals(disjoint) == [[1, 5]]

def test_min_meeting_rooms():
    meetings = [[0, 30], [5, 10], [15, 20]]
    assert IntervalSchedulingEngine.min_meeting_rooms(meetings) == 2

    no_overlap = [[7, 10], [2, 4]]
    assert IntervalSchedulingEngine.min_meeting_rooms(no_overlap) == 1

def test_erase_overlap_intervals():
    intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
    assert IntervalSchedulingEngine.erase_overlap_intervals(intervals) == 1

def test_empty_intervals():
    assert IntervalSchedulingEngine.merge_intervals([]) == []
    assert IntervalSchedulingEngine.min_meeting_rooms([]) == 0
    assert IntervalSchedulingEngine.erase_overlap_intervals([]) == 0

def test_single_interval():
    assert IntervalSchedulingEngine.merge_intervals([[1, 5]]) == [[1, 5]]
    assert IntervalSchedulingEngine.min_meeting_rooms([[1, 5]]) == 1
    assert IntervalSchedulingEngine.erase_overlap_intervals([[1, 5]]) == 0
