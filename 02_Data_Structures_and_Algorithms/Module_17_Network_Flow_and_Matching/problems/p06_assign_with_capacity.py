"""Problem 06 - Workers Who Can Take Several Shifts

Pattern:    Flow with non-unit capacities
Difficulty: Medium
Target:     Time O(V * E^2)

Each worker can cover up to ``shifts_each`` shifts; each shift needs
exactly one worker. Given who is available for which shift, return the largest
number of shifts that can be staffed.

Constraints
- ``1 <= workers, shifts <= 200``, ``1 <= shifts_each <= 50``

Example
    staff_shifts(2, 4, [(0,0),(0,1),(1,2),(1,3)], shifts_each=2) -> 4
    staff_shifts(2, 4, [(0,0),(0,1),(1,2),(1,3)], shifts_each=1) -> 2

One number changes and the answer halves. That number is a capacity, and knowing
*which* capacity encodes *which* rule is the whole skill this module teaches.

Example:
    >>> staff_shifts(2, 4, [(0, 0), (0, 1), (1, 2), (1, 3)], shifts_each=2)
    4
    >>> staff_shifts(2, 4, [(0, 0), (0, 1), (1, 2), (1, 3)], shifts_each=1)
    2

Hints - read one at a time, and try again between each.

    Hint 1: Start from the matching reduction in problem 03.
    Hint 2: The only thing that changes is the capacity on the source-to-worker edges.
    Hint 3: Shift-to-sink stays at 1, because a shift still needs exactly one worker.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def staff_shifts(workers: int, shifts: int, available: list[tuple[int, int]],
                 shifts_each: int) -> int:
    raise NotImplementedError("implement staff_shifts")
