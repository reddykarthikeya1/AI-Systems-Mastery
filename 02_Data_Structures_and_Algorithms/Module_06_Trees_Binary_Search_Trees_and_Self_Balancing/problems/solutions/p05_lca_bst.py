"""Reference solution — Problem 05: Lowest Common Ancestor In A BST

Pattern:    BST invariant walk
Complexity: Time O(height), Space O(1)
"""

from __future__ import annotations

from tree_common import TreeNode


def lca_bst(root: TreeNode | None, p: int, q: int) -> TreeNode | None:
    lo, hi = min(p, q), max(p, q)
    node = root
    while node is not None:
        if hi < node.val:
            node = node.left        # both on the left
        elif lo > node.val:
            node = node.right       # both on the right
        else:
            # They straddle this node, or one of them IS this node.
            return node
    return None
