"""Problem 08 — Diameter Of A Binary Tree

Pattern:    Bottom-up recursion with a running best
Difficulty: Hard
Target:     Time O(n), Space O(height)

Return the number of **edges** on the longest path between any two nodes. The
path need not pass through the root.

Constraints
- ``0 <= nodes <= 10**4``
- O(n) expected

Example
    from_level_order([1, 2, 3, 4, 5]) -> 3     (4 -> 2 -> 1 -> 3)

Example:
    >>> from tree_common import from_level_order
    >>> tree_diameter(from_level_order([1, 2, 3, 4, 5]))
    3

Hints — read one at a time, and try again between each.

    Hint 1: For each node, the longest path THROUGH it is left_height + right_height, counted in edges.
    Hint 2: The diameter is the maximum of that quantity over all nodes - which is not necessarily at the root.
    Hint 3: So return the height from the recursion, and keep the best through-path in a variable updated at every node. One pass, O(n).

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations

from tree_common import TreeNode


def tree_diameter(root: TreeNode | None) -> int:
    raise NotImplementedError("implement tree_diameter")
