"""Reference solution — Problem 06: K-th Smallest Element In A BST

Pattern:    Inorder with early exit
Complexity: Time O(height + k), Space O(height)
"""

from __future__ import annotations

from tree_common import TreeNode


def kth_smallest_bst(root: TreeNode | None, k: int) -> int:
    if k < 1:
        raise ValueError(f"k must be at least 1, got {k}")

    stack: list[TreeNode] = []
    node = root
    seen = 0

    while node is not None or stack:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        seen += 1
        if seen == k:
            return node.val         # stop as soon as the answer is known
        node = node.right

    raise ValueError(f"k={k} exceeds the {seen} nodes in the tree")
