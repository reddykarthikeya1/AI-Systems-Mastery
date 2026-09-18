"""Problem 03 — Maximum Depth

Pattern:    Tree recursion
Difficulty: Easy
Target:     Time O(n), Space O(height)

Return the number of nodes on the longest root-to-leaf path. An empty tree has
depth 0.

Constraints
- ``0 <= nodes <= 10**4``

Example
    from_level_order([3, 9, 20, None, None, 15, 7]) -> 3

Example:
    >>> from tree_common import from_level_order
    >>> max_depth(from_level_order([3, 9, 20, None, None, 15, 7]))
    3

Hints — read one at a time, and try again between each.

    Hint 1: The depth of a tree is one more than the depth of its deeper subtree.
    Hint 2: The base case is the empty tree, whose depth is 0 - not 1.
    Hint 3: return 1 + max(max_depth(left), max_depth(right)).

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations

from tree_common import TreeNode


def max_depth(root: TreeNode | None) -> int:
    raise NotImplementedError("implement max_depth")
