"""Problem 07 — Palindrome Linked List

Pattern:    Fast/slow + in-place reversal
Difficulty: Medium
Target:     Time O(n), Space O(1)

Return True if the list reads the same forwards and backwards.

Constraints
- ``0 <= length <= 10**5``
- O(1) extra space is the target — copying values into a Python list is O(n)

Example
    [1, 2, 2, 1] -> True
    [1, 2]       -> False

Hints — read one at a time, and try again between each.

    Hint 1: You cannot walk a singly linked list backwards. But you can reverse half of it.
    Hint 2: Find the middle with fast/slow, reverse the second half in place, then compare the two halves node by node.
    Hint 3: Stop comparing when the reversed half runs out - for odd lengths the middle element is unpaired and must simply be ignored.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations

from linked_list_common import ListNode


def is_palindrome_list(head: ListNode | None) -> bool:
    raise NotImplementedError("implement is_palindrome_list")
