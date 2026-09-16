"""Reference solution — Problem 07: Palindrome Linked List

Pattern:    Fast/slow + in-place reversal
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations

from linked_list_common import ListNode


def is_palindrome_list(head: ListNode | None) -> bool:
    if head is None or head.next is None:
        return True

    # Find the middle (second middle for even lengths).
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next            # type: ignore[union-attr]
        fast = fast.next.next

    # Reverse from the middle onwards.
    prev: ListNode | None = None
    cur = slow
    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    # Compare the two halves. `prev` is shorter or equal, so it controls the
    # loop; for odd lengths the unpaired middle is skipped naturally.
    left, right = head, prev
    while right is not None:
        if left.val != right.val:   # type: ignore[union-attr]
            return False
        left = left.next            # type: ignore[union-attr]
        right = right.next
    return True
