"""Reference solution — Problem 03: Maximum Depth

Pattern:    Tree recursion
Complexity: Time O(n), Space O(height)
"""

from __future__ import annotations

from tree_common import TreeNode


def max_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0
    # One for this node, plus whichever subtree runs deeper.
    return 1 + max(max_depth(root.left), max_depth(root.right))
