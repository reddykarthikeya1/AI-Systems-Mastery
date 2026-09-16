"""Starter template for AVLTreeEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class AVLNode(Generic[T]):
    def __init__(self, val: T):
        self.val = val
        self.height = 1
        self.left: AVLNode[T] | None = None
        self.right: AVLNode[T] | None = None

class AVLTreeEngine(Generic[T]):
    """Self-balancing AVL Binary Search Tree."""

    def __init__(self) -> None:
        raise NotImplementedError

    def insert(self, val: T) -> None:
        raise NotImplementedError

    def contains(self, val: T) -> bool:
        raise NotImplementedError

    def in_order(self) -> list[T]:
        raise NotImplementedError

    def validate_invariants(self) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
