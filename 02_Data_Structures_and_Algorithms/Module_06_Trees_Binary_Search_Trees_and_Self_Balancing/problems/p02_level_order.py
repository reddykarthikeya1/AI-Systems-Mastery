"""Problem 02 — Level Order Traversal

Pattern:    BFS
Difficulty: Medium
Target:     Time O(n), Space O(width)

Return the node values grouped by depth, top to bottom.

Constraints
- ``0 <= nodes <= 2000``

Example
    from_level_order([3, 9, 20, None, None, 15, 7]) -> [[3], [9, 20], [15, 7]]

Example:
    >>> from tree_common import from_level_order
    >>> level_order(from_level_order([3, 9, 20, None, None, 15, 7]))
    [[3], [9, 20], [15, 7]]

Hints — read one at a time, and try again between each.

    Hint 1: Breadth-first with a queue visits nodes in exactly this order.
    Hint 2: But a plain BFS gives you one flat list. You need to know where each level ends.
    Hint 3: Record len(queue) at the top of each iteration - that is exactly the number of nodes on the current level - then pop that many.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations

from tree_common import TreeNode


def level_order(root: TreeNode | None) -> list[list[int]]:
    raise NotImplementedError("implement level_order")
