"""Reference solution — Problem 04: Validate A Binary Search Tree

Pattern:    Range invariant propagation
Complexity: Time O(n), Space O(height)
"""

from __future__ import annotations

from tree_common import TreeNode


def is_valid_bst(root: TreeNode | None) -> bool:
    def check(node: TreeNode | None, low: float, high: float) -> bool:
        if node is None:
            return True
        # The bounds accumulated from EVERY ancestor, not just the parent.
        if not (low < node.val < high):
            return False
        return check(node.left, low, node.val) and check(node.right, node.val, high)

    return check(root, float("-inf"), float("inf"))
