"""Problem 08 — Reorder List

Pattern:    Split + reverse + weave
Difficulty: Hard
Target:     Time O(n), Space O(1)

Reorder the list so the nodes appear in the order
first, last, second, second-to-last, third, … Return the head.

Reorder in place by relinking nodes; do not allocate new ones.

Constraints
- ``0 <= length <= 5 * 10**4``

Example
    [1, 2, 3, 4]    -> [1, 4, 2, 3]
    [1, 2, 3, 4, 5] -> [1, 5, 2, 4, 3]

Example:
    >>> from linked_list_common import from_list, to_list
    >>> to_list(reorder_list(from_list([1, 2, 3, 4])))
    [1, 4, 2, 3]

Hints — read one at a time, and try again between each.

    Hint 1: This is three problems you have already solved, composed: find the middle, reverse a list, merge two lists by alternating.
    Hint 2: Split at the middle, reverse the second half, then weave.
    Hint 3: Cut the first half's link to the second before reversing, or the 'reversed' half still points back into the first half and you build a cycle. That is the bug this problem is really testing.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations

from linked_list_common import ListNode


def reorder_list(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError("implement reorder_list")
