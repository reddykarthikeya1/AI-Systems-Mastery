"""Reference solution — Problem 06: Minimum Meeting Rooms

Pattern:    Heap of end times
Complexity: Time O(n log n), Space O(n)
"""

from __future__ import annotations


def min_meeting_rooms(intervals: list[tuple[int, int]]) -> int:
    import heapq

    if not intervals:
        return 0

    # Earliest start first; the heap holds the end times of occupied rooms.
    ends: list[int] = []
    for start, end in sorted(intervals):
        # A room freed exactly at `start` can be reused, hence <=.
        if ends and ends[0] <= start:
            heapq.heappop(ends)
        heapq.heappush(ends, end)

    return len(ends)
