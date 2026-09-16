"""Reference solution — Problem 02: Level Order Traversal

Pattern:    BFS
Complexity: Time O(n), Space O(width)
"""

from __future__ import annotations

from tree_common import TreeNode


def level_order(root: TreeNode | None) -> list[list[int]]:
    from collections import deque

    if root is None:
        return []

    out: list[list[int]] = []
    queue = deque([root])

    while queue:
        # Snapshot the width BEFORE adding children, which is what separates
        # the levels.
        level_size = len(queue)
        level: list[int] = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        out.append(level)

    return out
