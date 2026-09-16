"""Reference solution — Problem 03: Find Where The Cycle Begins

Pattern:    Floyd's algorithm
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations

from linked_list_common import ListNode


def cycle_start(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    # Phase 1: find a meeting point inside the cycle.
    while fast is not None and fast.next is not None:
        slow = slow.next            # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None                 # fell out of the loop - no cycle
    if fast is None or fast.next is None:
        return None

    # Phase 2: the distance from head to the entrance equals the distance from
    # the meeting point to the entrance, so equal-speed pointers converge there.
    finder = head
    while finder is not slow:
        finder = finder.next        # type: ignore[union-attr]
        slow = slow.next            # type: ignore[union-attr]
    return finder
