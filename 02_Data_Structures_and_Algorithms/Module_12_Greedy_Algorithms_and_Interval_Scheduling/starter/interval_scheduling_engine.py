"""Starter template for IntervalSchedulingEngine."""
from __future__ import annotations


class IntervalSchedulingEngine:
    """Greedy interval scheduling and sweep-line algorithms."""

    @staticmethod
    def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
        """Merge all overlapping intervals."""
        raise NotImplementedError

    @staticmethod
    def min_meeting_rooms(intervals: list[list[int]]) -> int:
        """Find min conference rooms required using sweep-line or min-heap."""
        raise NotImplementedError

    @staticmethod
    def erase_overlap_intervals(intervals: list[list[int]]) -> int:
        """Min intervals to remove to make remainder non-overlapping."""
        raise NotImplementedError
