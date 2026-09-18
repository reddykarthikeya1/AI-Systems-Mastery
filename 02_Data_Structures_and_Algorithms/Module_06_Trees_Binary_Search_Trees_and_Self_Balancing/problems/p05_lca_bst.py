"""Problem 05 — Lowest Common Ancestor In A BST

Pattern:    BST invariant walk
Difficulty: Medium
Target:     Time O(height), Space O(1)

Return the lowest node that has both ``p`` and ``q`` as descendants (a node may
be a descendant of itself). Both values are present in the tree.

Constraints
- ``2 <= nodes <= 10**5``
- the tree is a valid BST with distinct values
- O(height) expected — do not search the whole tree

Example
    tree [6,2,8,0,4,7,9], p=2, q=8 -> node 6
    tree [6,2,8,0,4,7,9], p=2, q=4 -> node 2

Example:
    >>> from tree_common import from_level_order
    >>> lca_bst(from_level_order([6, 2, 8, 0, 4, 7, 9]), 2, 8).val
    6
    >>> lca_bst(from_level_order([6, 2, 8, 0, 4, 7, 9]), 2, 4).val
    2

Hints — read one at a time, and try again between each.

    Hint 1: In a general binary tree this needs a full search. A BST gives you far more: the ordering tells you which way to go.
    Hint 2: If both values are less than the current node, the answer is in the left subtree. If both are greater, it is in the right.
    Hint 3: Otherwise the values straddle the current node (or one equals it), and the current node IS the lowest common ancestor. No recursion needed - a while loop suffices.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations

from tree_common import TreeNode


def lca_bst(root: TreeNode | None, p: int, q: int) -> TreeNode | None:
    raise NotImplementedError("implement lca_bst")
