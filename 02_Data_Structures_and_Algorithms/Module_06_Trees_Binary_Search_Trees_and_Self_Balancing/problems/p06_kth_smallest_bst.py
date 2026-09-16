"""Problem 06 — K-th Smallest Element In A BST

Pattern:    Inorder with early exit
Difficulty: Medium
Target:     Time O(height + k), Space O(height)

Return the ``k``-th smallest value (1-indexed). Raise ``ValueError`` if ``k`` is
out of range.

Constraints
- ``1 <= k <= nodes <= 10**4``
- must stop as soon as the answer is known — do not materialise the whole
  traversal when k is 1

Example
    tree [3, 1, 4, None, 2], k = 1 -> 1
    tree [5, 3, 6, 2, 4, None, None, 1], k = 3 -> 3

Hints — read one at a time, and try again between each.

    Hint 1: A BST's inorder traversal is sorted. So the k-th smallest is the k-th node visited inorder.
    Hint 2: Building the full traversal and indexing works but is O(n) even when k = 1.
    Hint 3: Use the iterative inorder from problem 01 and return the moment you have popped k nodes. That is O(height + k).

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations

from tree_common import TreeNode


def kth_smallest_bst(root: TreeNode | None, k: int) -> int:
    raise NotImplementedError("implement kth_smallest_bst")
