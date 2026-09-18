"""Problem 03 — Find Where The Cycle Begins

Pattern:    Floyd's algorithm
Difficulty: Medium
Target:     Time O(n), Space O(1)

Return the node where the cycle begins, or None if there is no cycle.

Constraints
- ``0 <= length <= 10**4``
- O(1) extra space

Example
    build_cycle([3, 2, 0, -4], 1) -> the node with value 2

Example:
    >>> from linked_list_common import build_cycle
    >>> cycle_start(build_cycle([3, 2, 0, -4], 1)).val
    2

Hints — read one at a time, and try again between each.

    Hint 1: First detect the cycle with fast/slow, exactly as in problem 02.
    Hint 2: Now the arithmetic: if the cycle starts at distance F from the head and the meeting point is distance a into the cycle, then F == (cycle length - a) mod cycle length.
    Hint 3: Which means: reset one pointer to the head, leave the other at the meeting point, and advance BOTH one step at a time. They meet at the cycle entrance.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations

from linked_list_common import ListNode


def cycle_start(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError("implement cycle_start")
