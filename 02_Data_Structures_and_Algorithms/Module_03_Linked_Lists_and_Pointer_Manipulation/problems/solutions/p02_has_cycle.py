"""Reference solution — Problem 02: Detect A Cycle

Pattern:    Fast and slow pointers
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations

from linked_list_common import ListNode


def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next          # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            return True
    return False
