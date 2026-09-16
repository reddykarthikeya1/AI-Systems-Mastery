"""Shared binary-tree scaffolding for Module 06's problems.

Plumbing, not an exercise. ``from_level_order`` lets the tests state a tree as a
flat list with ``None`` for absent children, which keeps the assertions readable.
"""

from __future__ import annotations

from collections import deque


class TreeNode:
    __slots__ = ("left", "right", "val")

    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


def from_level_order(values: list[int | None]) -> TreeNode | None:
    """Build a tree from a level-order list, using None for a missing child.

    ``[3, 9, 20, None, None, 15, 7]`` builds::

            3
           / \
          9  20
             / \
            15  7
    """
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])          # type: ignore[arg-type]
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.left = TreeNode(v)
                queue.append(node.left)
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.right = TreeNode(v)
                queue.append(node.right)
    return root


def to_level_order(root: TreeNode | None) -> list[int | None]:
    """Flatten back to a level-order list with trailing Nones stripped."""
    if root is None:
        return []
    out: list[int | None] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def find_node(root: TreeNode | None, val: int) -> TreeNode | None:
    if root is None:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)
