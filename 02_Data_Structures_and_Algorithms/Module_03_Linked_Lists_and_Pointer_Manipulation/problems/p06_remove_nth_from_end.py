"""Problem 06 — Remove The N-th Node From The End

Pattern:    Dummy head + gap pointers
Difficulty: Medium
Target:     Time O(n), Space O(1)

Remove the ``n``-th node counting from the end and return the head.

Constraints
- ``1 <= n <= length <= 30``
- one pass

Example
    [1, 2, 3, 4, 5], n = 2 -> [1, 2, 3, 5]
    [1], n = 1             -> []

Hints — read one at a time, and try again between each.

    Hint 1: Two pointers with a fixed gap of n between them: when the leader hits the end, the follower is at the node before the one to remove.
    Hint 2: Removing the head is the awkward case. A dummy node in front of the head makes it identical to every other case.
    Hint 3: Start both pointers at the dummy, advance the leader n+1 times, then advance both until the leader is None.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations

from linked_list_common import ListNode


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    raise NotImplementedError("implement remove_nth_from_end")
