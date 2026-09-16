"""Reference solution — Problem 05: Merge Two Sorted Lists

Pattern:    Dummy head + two pointers
Complexity: Time O(n + m), Space O(1)
"""

from __future__ import annotations

from linked_list_common import ListNode


def merge_sorted(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    dummy = ListNode(0)     # throwaway: removes the 'which head?' special case
    tail = dummy

    while a is not None and b is not None:
        # <= rather than < keeps the merge stable when values tie.
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    # At most one list remains; splice it on wholesale.
    tail.next = a if a is not None else b
    return dummy.next
