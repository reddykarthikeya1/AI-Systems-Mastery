"""Problem 04 — Validate A Binary Search Tree

Pattern:    Range invariant propagation
Difficulty: Medium
Target:     Time O(n), Space O(height)

Return True if the tree is a valid binary search tree: **every** node in a
node's left subtree is strictly less than it, and every node in its right
subtree is strictly greater.

Constraints
- ``0 <= nodes <= 10**4``
- values are distinct

Example
    from_level_order([2, 1, 3])          -> True
    from_level_order([5, 1, 4, None, None, 3, 6]) -> False

The second example is the whole point. Node 4's children (3 and 6) satisfy a
local check, but 3 sits in 5's right subtree while being less than 5. Comparing
only against immediate children accepts this tree, and it is not a BST.

Example:
    >>> from tree_common import from_level_order
    >>> is_valid_bst(from_level_order([2, 1, 3]))
    True
    >>> is_valid_bst(from_level_order([5, 1, 4, None, None, 3, 6]))
    False

Hints — read one at a time, and try again between each.

    Hint 1: Checking node.left.val < node.val < node.right.val is not enough - it is a local test for a global property.
    Hint 2: Every node is constrained by ALL of its ancestors, not just its parent. Descending left tightens the upper bound; descending right tightens the lower bound.
    Hint 3: Carry (low, high) down the recursion. A node must satisfy low < val < high, and it passes (low, val) left and (val, high) right.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations

from tree_common import TreeNode


def is_valid_bst(root: TreeNode | None) -> bool:
    raise NotImplementedError("implement is_valid_bst")
