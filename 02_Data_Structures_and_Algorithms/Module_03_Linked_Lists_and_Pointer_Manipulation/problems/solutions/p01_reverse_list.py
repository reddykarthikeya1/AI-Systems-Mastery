"""Reference solution — Problem 01: Reverse A Linked List

Pattern:    Pointer manipulation
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations

from linked_list_common import ListNode


def reverse_list(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None
    cur = head
    while cur is not None:
        nxt = cur.next      # save it first - the next line destroys this link
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
