"""Problem 02 — Detect A Cycle

Pattern:    Fast and slow pointers
Difficulty: Easy
Target:     Time O(n), Space O(1)

Return True if the list contains a cycle.

Constraints
- ``0 <= length <= 10**4``
- must be O(1) extra space — a ``set`` of visited nodes is O(n) and does not count

Example
    build_cycle([3, 2, 0, -4], 1) -> True
    build_cycle([1, 2], -1)       -> False

Hints — read one at a time, and try again between each.

    Hint 1: Two runners on a circular track, one twice as fast as the other, must eventually meet.
    Hint 2: Advance slow by one node and fast by two each step.
    Hint 3: If fast (or fast.next) reaches None there is no cycle. Check those BEFORE dereferencing, or you get an AttributeError on a list of length 1.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations

from linked_list_common import ListNode


def has_cycle(head: ListNode | None) -> bool:
    raise NotImplementedError("implement has_cycle")
