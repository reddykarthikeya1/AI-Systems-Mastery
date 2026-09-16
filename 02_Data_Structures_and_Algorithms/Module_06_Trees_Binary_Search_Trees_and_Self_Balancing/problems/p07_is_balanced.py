"""Problem 07 — Height-Balanced Binary Tree

Pattern:    Bottom-up recursion
Difficulty: Medium
Target:     Time O(n), Space O(height)

Return True if, for **every** node, the heights of its two subtrees differ by at
most 1.

Constraints
- ``0 <= nodes <= 5000``
- O(n) expected

Example
    from_level_order([3, 9, 20, None, None, 15, 7])       -> True
    from_level_order([1, 2, 2, 3, 3, None, None, 4, 4])   -> False

A note on recursion depth: the idiomatic solution here is recursive, and Python's
default limit is 1000 frames. A degenerate tree deeper than that raises
``RecursionError`` rather than returning an answer. That is a real property of
the solution, not a trick — if you need to survive a 5000-deep spine, either
call ``sys.setrecursionlimit`` deliberately or rewrite the traversal with an
explicit stack, as Problem 01 does.

Hints — read one at a time, and try again between each.

    Hint 1: The obvious solution computes the height at every node, which recomputes the same subtree heights over and over - that is O(n^2) on a skewed tree.
    Hint 2: Compute the height and the balance verdict in the SAME pass, bottom-up.
    Hint 3: Have the recursion return the height, or a sentinel like -1 meaning 'already unbalanced', and propagate the sentinel upward.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations

from tree_common import TreeNode


def is_balanced(root: TreeNode | None) -> bool:
    raise NotImplementedError("implement is_balanced")
