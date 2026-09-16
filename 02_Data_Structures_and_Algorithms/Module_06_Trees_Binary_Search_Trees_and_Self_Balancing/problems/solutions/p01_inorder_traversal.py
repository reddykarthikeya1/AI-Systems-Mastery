"""Reference solution — Problem 01: Iterative Inorder Traversal

Pattern:    Explicit stack traversal
Complexity: Time O(n), Space O(height)
"""

from __future__ import annotations

from tree_common import TreeNode


def inorder_traversal(root: TreeNode | None) -> list[int]:
    out: list[int] = []
    stack: list[TreeNode] = []
    node = root

    while node is not None or stack:
        # Descend to the leftmost unvisited node, remembering the path.
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        # Everything left of and including `node` is done; go right.
        node = node.right

    return out
