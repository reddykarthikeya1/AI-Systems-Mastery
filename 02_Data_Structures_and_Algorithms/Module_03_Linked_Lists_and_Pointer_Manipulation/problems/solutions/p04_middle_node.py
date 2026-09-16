"""Reference solution — Problem 04: Middle Of The List

Pattern:    Fast and slow pointers
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations

from linked_list_common import ListNode


def middle_node(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    # This condition yields the SECOND middle for even lengths, which is what
    # was asked. Starting `fast` one node ahead would yield the first.
    while fast is not None and fast.next is not None:
        slow = slow.next            # type: ignore[union-attr]
        fast = fast.next.next
    return slow
