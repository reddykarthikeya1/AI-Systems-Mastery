"""Problem 03 — Longest Consecutive Sequence

Pattern:    Hash set + sequence-start check
Difficulty: Medium
Target:     Time O(n), Space O(n)

Return the length of the longest run of consecutive integers present in
``nums``. The numbers need not be adjacent in the array.

Constraints
- ``0 <= len(nums) <= 10**5``
- **O(n) expected** — sorting would be O(n log n), which is the obvious answer
  and not the one being asked for

Example
    longest_consecutive([100, 4, 200, 1, 3, 2]) -> 4    (1, 2, 3, 4)

Example:
    >>> longest_consecutive([100, 4, 200, 1, 3, 2])
    4

Hints — read one at a time, and try again between each.

    Hint 1: Put everything in a set so membership is O(1).
    Hint 2: Now you could walk outward from every element, but that re-walks the same run once per member - O(n^2) in the worst case.
    Hint 3: Only start counting from a value that BEGINS a run, i.e. one where x - 1 is not in the set. Every run is then walked exactly once, so the total is O(n) despite the nested loop.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def longest_consecutive(nums: list[int]) -> int:
    raise NotImplementedError("implement longest_consecutive")
