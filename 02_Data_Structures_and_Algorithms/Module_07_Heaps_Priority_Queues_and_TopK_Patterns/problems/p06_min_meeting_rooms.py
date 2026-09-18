"""Problem 06 — Minimum Meeting Rooms

Pattern:    Heap of end times
Difficulty: Medium
Target:     Time O(n log n), Space O(n)

Given meeting ``(start, end)`` intervals, return the minimum number of rooms
needed so that no two meetings overlap in a room. A meeting ending at time ``t``
frees the room for one starting at ``t``.

Constraints
- ``0 <= len(intervals) <= 10**4``
- ``0 <= start < end``

Example
    min_meeting_rooms([(0, 30), (5, 10), (15, 20)]) -> 2
    min_meeting_rooms([(7, 10), (2, 4)])            -> 1

Example:
    >>> min_meeting_rooms([(0, 30), (5, 10), (15, 20)])
    2
    >>> min_meeting_rooms([(7, 10), (2, 4)])
    1

Hints — read one at a time, and try again between each.

    Hint 1: Process meetings in order of start time - so sort first.
    Hint 2: For each new meeting you only care whether ANY room is free, which means you only care about the earliest end time among occupied rooms.
    Hint 3: Keep those end times in a min-heap. If the earliest end is <= the new start, reuse that room (pop); otherwise allocate a new one. The heap's maximum size is the answer.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def min_meeting_rooms(intervals: list[tuple[int, int]]) -> int:
    raise NotImplementedError("implement min_meeting_rooms")
