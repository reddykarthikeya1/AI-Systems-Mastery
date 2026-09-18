"""Problem 04 — K Closest Points To The Origin

Pattern:    Max-heap of size k
Difficulty: Medium
Target:     Time O(n log k), Space O(k)

Return the ``k`` points closest to the origin, ordered by increasing distance.
Break ties by ``x`` then ``y`` so the output is deterministic.

Constraints
- ``1 <= k <= len(points) <= 10**5``
- target O(n log k)

Example
    k_closest_points([(1, 3), (-2, 2)], 1) -> [(-2, 2)]

Example:
    >>> k_closest_points([(1, 3), (-2, 2)], 1)
    [(-2, 2)]

Hints — read one at a time, and try again between each.

    Hint 1: You never need the actual distance - only the ordering. So skip the square root and compare x*x + y*y, which also keeps everything in integers and avoids float error.
    Hint 2: You want the k SMALLEST distances, so keep a heap whose root is the LARGEST of your current best k - the opposite of problem 01.
    Hint 3: Python's heapq is a min-heap, so push negated distances. At the end, sort the k survivors for the required output order.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def k_closest_points(points: list[tuple[int, int]], k: int) -> list[tuple[int, int]]:
    raise NotImplementedError("implement k_closest_points")
