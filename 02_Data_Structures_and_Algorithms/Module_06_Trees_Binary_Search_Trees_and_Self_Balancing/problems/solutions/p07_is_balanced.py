"""Reference solution — Problem 07: Height-Balanced Binary Tree

Pattern:    Bottom-up recursion
Complexity: Time O(n), Space O(height)
"""

from __future__ import annotations

from tree_common import TreeNode


def is_balanced(root: TreeNode | None) -> bool:
    UNBALANCED = -1

    def height(node: TreeNode | None) -> int:
        if node is None:
            return 0
        left = height(node.left)
        if left == UNBALANCED:
            return UNBALANCED       # propagate, do not keep measuring
        right = height(node.right)
        if right == UNBALANCED:
            return UNBALANCED
        if abs(left - right) > 1:
            return UNBALANCED
        return 1 + max(left, right)

    return height(root) != UNBALANCED
