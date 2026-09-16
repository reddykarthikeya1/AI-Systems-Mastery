"""Problem 04 — Middle Of The List

Pattern:    Fast and slow pointers
Difficulty: Easy
Target:     Time O(n), Space O(1)

Return the middle node. If the list has an even number of nodes, return the
**second** of the two middle nodes.

Constraints
- ``0 <= length <= 10**4``
- one pass, O(1) extra space — do not count the length first

Example
    [1, 2, 3, 4, 5]    -> node 3
    [1, 2, 3, 4, 5, 6] -> node 4

Hints — read one at a time, and try again between each.

    Hint 1: Move one pointer twice as fast as the other.
    Hint 2: When the fast pointer runs off the end, the slow one is at the middle.
    Hint 3: The loop condition decides which middle you get for even lengths. `while fast and fast.next` returns the second middle; starting fast at head.next returns the first. Check which the problem asked for.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations

from linked_list_common import ListNode


def middle_node(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError("implement middle_node")
