"""Problem 01 — Reverse A Linked List

Pattern:    Pointer manipulation
Difficulty: Easy
Target:     Time O(n), Space O(1)

Reverse a singly linked list in place and return the new head.

Constraints
- ``0 <= length <= 5000``
- must be O(1) extra space — no building a Python list and rebuilding

Example
    [1, 2, 3] -> [3, 2, 1]

Example:
    >>> from linked_list_common import from_list, to_list
    >>> to_list(reverse_list(from_list([1, 2, 3])))
    [3, 2, 1]

Hints — read one at a time, and try again between each.

    Hint 1: You need three pointers: previous, current, and the next node.
    Hint 2: Save current.next BEFORE you overwrite it, or you lose the rest of the list and cannot get it back.
    Hint 3: Loop: nxt = cur.next; cur.next = prev; prev = cur; cur = nxt. When cur is None, prev is the new head.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations

from linked_list_common import ListNode


def reverse_list(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError("implement reverse_list")
