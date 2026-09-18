"""Problem 05 — Merge Two Sorted Lists

Pattern:    Dummy head + two pointers
Difficulty: Easy
Target:     Time O(n + m), Space O(1)

Merge two sorted linked lists into one sorted list by splicing the existing
nodes. Return the new head.

Constraints
- ``0 <= len(a), len(b) <= 50``
- must be stable: when values tie, take from ``a`` first
- O(1) extra space — splice, do not allocate new nodes

Example
    [1, 2, 4] + [1, 3, 4] -> [1, 1, 2, 3, 4, 4]

Example:
    >>> from linked_list_common import from_list, to_list
    >>> to_list(merge_sorted(from_list([1, 2, 4]), from_list([1, 3, 4])))
    [1, 1, 2, 3, 4, 4]

Hints — read one at a time, and try again between each.

    Hint 1: Handling 'which list does the head come from?' as a special case is where the bugs live.
    Hint 2: Allocate one throwaway dummy node, build the result after it, and return dummy.next. Now there is no special case at all.
    Hint 3: For stability on ties, take from `a` when a.val <= b.val - the <= is what makes it stable.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations

from linked_list_common import ListNode


def merge_sorted(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    raise NotImplementedError("implement merge_sorted")
