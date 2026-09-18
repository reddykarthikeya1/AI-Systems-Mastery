"""Problem 01 — Iterative Inorder Traversal

Pattern:    Explicit stack traversal
Difficulty: Medium
Target:     Time O(n), Space O(height)

Return the values in inorder (left, node, right) **without recursion**.

Constraints
- ``0 <= nodes <= 10**4`` — deep enough that recursion could exceed Python's
  1000-frame default limit

Example
    from_level_order([1, None, 2, 3]) -> [1, 3, 2]

Example:
    >>> from tree_common import from_level_order
    >>> inorder_traversal(from_level_order([1, None, 2, 3]))
    [1, 3, 2]

Hints — read one at a time, and try again between each.

    Hint 1: Recursion uses the call stack. Doing it iteratively means managing that stack yourself.
    Hint 2: Walk as far left as possible, pushing every node you pass.
    Hint 3: Then pop, record the value, and move to the popped node's right child - repeating the leftward walk from there.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations

from tree_common import TreeNode


def inorder_traversal(root: TreeNode | None) -> list[int]:
    raise NotImplementedError("implement inorder_traversal")
