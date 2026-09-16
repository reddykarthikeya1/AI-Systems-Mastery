"""Production solution for IntervalSchedulingEngine."""
from __future__ import annotations

import heapq


class IntervalSchedulingEngine:
    """Greedy interval processing algorithms."""

    @staticmethod
    def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
        if not intervals:
            return []

        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        merged: list[list[int]] = [sorted_intervals[0]]

        for start, end in sorted_intervals[1:]:
            last_start, last_end = merged[-1]
            if start <= last_end:
                merged[-1] = [last_start, max(last_end, end)]
            else:
                merged.append([start, end])

        return merged

    @staticmethod
    def min_meeting_rooms(intervals: list[list[int]]) -> int:
        if not intervals:
            return 0

        # Sort intervals by start time
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        # Min-heap storing end times of ongoing meetings
        room_end_times: list[int] = []

        for start, end in sorted_intervals:
            if room_end_times and room_end_times[0] <= start:
                heapq.heappop(room_end_times)
            heapq.heappush(room_end_times, end)

        return len(room_end_times)

    @staticmethod
    def erase_overlap_intervals(intervals: list[list[int]]) -> int:
        """Greedy selection: always pick interval that ends earliest."""
        if not intervals:
            return 0

        # Sort by end time
        sorted_intervals = sorted(intervals, key=lambda x: x[1])
        count_removed = 0
        last_end = float("-inf")

        for start, end in sorted_intervals:
            if start >= last_end:
                last_end = end
            else:
                count_removed += 1

        return count_removed
