"""Reference solution — Problem 08: Reorder List

Pattern:    Split + reverse + weave
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations

from linked_list_common import ListNode


def reorder_list(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head

    # 1. Find the middle. `slow` ends on the LAST node of the first half.
    slow, fast = head, head.next
    while fast is not None and fast.next is not None:
        slow = slow.next            # type: ignore[union-attr]
        fast = fast.next.next

    second = slow.next
    slow.next = None                # cut: without this the weave builds a cycle

    # 2. Reverse the second half.
    prev: ListNode | None = None
    cur = second
    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    # 3. Weave. The first half is never shorter than the reversed second half.
    first, second = head, prev
    while second is not None:
        f_next, s_next = first.next, second.next   # type: ignore[union-attr]
        first.next = second                        # type: ignore[union-attr]
        second.next = f_next
        first, second = f_next, s_next

    return head
