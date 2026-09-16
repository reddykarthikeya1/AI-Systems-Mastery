"""Production solution for AVLTreeEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class AVLNode(Generic[T]):
    __slots__ = ("height", "left", "right", "val")

    def __init__(self, val: T):
        self.val = val
        self.height: int = 1
        self.left: AVLNode[T] | None = None
        self.right: AVLNode[T] | None = None

class AVLTreeEngine(Generic[T]):
    """Self-balancing AVL Tree guaranteeing O(log N) operations."""

    def __init__(self) -> None:
        self.root: AVLNode[T] | None = None
        self._size: int = 0

    def _get_height(self, node: AVLNode[T] | None) -> int:
        return node.height if node else 0

    def _get_balance(self, node: AVLNode[T] | None) -> int:
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _update_height(self, node: AVLNode[T]) -> None:
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _rotate_right(self, y: AVLNode[T]) -> AVLNode[T]:
        x = y.left
        assert x is not None
        t2 = x.right
        x.right = y
        y.left = t2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode[T]) -> AVLNode[T]:
        y = x.right
        assert y is not None
        t2 = y.left
        y.left = x
        x.right = t2
        self._update_height(x)
        self._update_height(y)
        return y

    def insert(self, val: T) -> None:
        self.root = self._insert_node(self.root, val)
        self._size += 1

    def _insert_node(self, node: AVLNode[T] | None, val: T) -> AVLNode[T]:
        if not node:
            return AVLNode(val)

        if val < node.val:
            node.left = self._insert_node(node.left, val)
        else:
            node.right = self._insert_node(node.right, val)

        self._update_height(node)
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and node.left and val < node.left.val:
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and node.right and val >= node.right.val:
            return self._rotate_left(node)

        # Left Right Case
        if balance > 1 and node.left and val >= node.left.val:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left Case
        if balance < -1 and node.right and val < node.right.val:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def contains(self, val: T) -> bool:
        curr = self.root
        while curr:
            if curr.val == val:
                return True
            curr = curr.left if val < curr.val else curr.right
        return False

    def in_order(self) -> list[T]:
        res: list[T] = []
        def _dfs(node: AVLNode[T] | None):
            if not node:
                return
            _dfs(node.left)
            res.append(node.val)
            _dfs(node.right)
        _dfs(self.root)
        return res

    def validate_invariants(self) -> bool:
        def _check(node: AVLNode[T] | None) -> tuple[bool, int]:
            if not node:
                return True, 0
            left_ok, left_h = _check(node.left)
            right_ok, right_h = _check(node.right)
            if not left_ok or not right_ok:
                return False, 0
            if abs(left_h - right_h) > 1:
                return False, 0
            actual_h = 1 + max(left_h, right_h)
            if node.height != actual_h:
                return False, 0
            return True, actual_h
        ok, _ = _check(self.root)
        return ok

    def __len__(self) -> int:
        return self._size
