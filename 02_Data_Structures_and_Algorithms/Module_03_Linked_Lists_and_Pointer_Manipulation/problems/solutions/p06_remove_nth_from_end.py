"""Reference solution — Problem 06: Remove The N-th Node From The End

Pattern:    Dummy head + gap pointers
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations

from linked_list_common import ListNode


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)   # makes removing the real head a normal case
    lead = lag = dummy

    # Open a gap of exactly n+1 so that `lag` ends up BEFORE the target.
    for _ in range(n + 1):
        if lead is None:
            return head          # n larger than the list - nothing to remove
        lead = lead.next

    while lead is not None:
        lead = lead.next
        lag = lag.next           # type: ignore[union-attr]

    lag.next = lag.next.next     # type: ignore[union-attr]
    return dummy.next
