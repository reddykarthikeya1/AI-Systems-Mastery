"""Reference solution — Problem 08: Diameter Of A Binary Tree

Pattern:    Bottom-up recursion with a running best
Complexity: Time O(n), Space O(height)
"""

from __future__ import annotations

from tree_common import TreeNode


def tree_diameter(root: TreeNode | None) -> int:
    best = 0

    def height(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        # Longest path passing through this node, measured in edges.
        best = max(best, left + right)
        return 1 + max(left, right)

    height(root)
    return best
