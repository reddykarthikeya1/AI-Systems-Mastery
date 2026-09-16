"""Starter template for the Fenwick tree and the treap.

Implement each piece, then run the shipped tests against your work:

    cd starter
    python -m pytest ../project_solution -q

They must FAIL until you have written the code.

Order that works: `FenwickTree.add` and `prefix_sum` first (they are four lines
each and everything else builds on them), then `from_values`, `range_sum`,
`find_kth`, `count_inversions`. The treap after that: `merge` and `split` first,
because `insert` and `erase` are written in terms of them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class FenwickTree:
    """Point update, prefix sum, both O(log n). One flat array, no nodes.

    The whole structure rests on `i & -i`, which isolates the lowest set bit of
    `i`. Index `i` stores the sum of the `i & -i` elements ending at `i`.
    """

    def __init__(self, size: int) -> None:
        raise NotImplementedError("implement FenwickTree.__init__")

    @classmethod
    def from_values(cls, values: list[int]) -> FenwickTree:
        """Build in O(n), not n separate O(log n) updates."""
        raise NotImplementedError("implement FenwickTree.from_values")

    def add(self, index: int, delta: int) -> None:
        """Add `delta` at `index`. Walk upward: i += i & -i."""
        raise NotImplementedError("implement FenwickTree.add")

    def prefix_sum(self, count: int) -> int:
        """Sum of indices [0, count). Walk downward: i -= i & -i."""
        raise NotImplementedError("implement FenwickTree.prefix_sum")

    def range_sum(self, start: int, stop: int) -> int:
        """Sum over the half-open interval [start, stop)."""
        raise NotImplementedError("implement FenwickTree.range_sum")

    def find_kth(self, k: int) -> int:
        """Smallest index whose prefix sum exceeds k, when values are counts.

        Binary lifting down the tree - O(log n), not O(log^2 n) from binary
        searching over prefix_sum.
        """
        raise NotImplementedError("implement FenwickTree.find_kth")


def count_inversions(values: list[int]) -> int:
    """Pairs (i, j) with i < j and values[i] > values[j]. O(n log n)."""
    raise NotImplementedError("implement count_inversions")


@dataclass
class TreapNode:
    key: Any
    priority: float
    size: int = 1
    left: TreapNode | None = field(default=None)
    right: TreapNode | None = field(default=None)


def merge(low: TreapNode | None, high: TreapNode | None) -> TreapNode | None:
    """Join two treaps where every key in `low` is below every key in `high`."""
    raise NotImplementedError("implement merge")


def split(node: TreapNode | None, key: Any) -> tuple[TreapNode | None, TreapNode | None]:
    """Cut into (keys < key, keys >= key)."""
    raise NotImplementedError("implement split")


class Treap:
    """An ordered set with order statistics, balanced by randomness alone."""

    def __init__(self, seed: int | None = None) -> None:
        raise NotImplementedError("implement Treap.__init__")

    def __len__(self) -> int:
        raise NotImplementedError("implement Treap.__len__")

    def __contains__(self, key: Any) -> bool:
        raise NotImplementedError("implement Treap.__contains__")

    def insert(self, key: Any) -> bool:
        raise NotImplementedError("implement Treap.insert")

    def erase(self, key: Any) -> bool:
        raise NotImplementedError("implement Treap.erase")

    def kth(self, k: int) -> Any:
        """The k-th smallest key, 0-based. Uses the subtree sizes."""
        raise NotImplementedError("implement Treap.kth")

    def rank(self, key: Any) -> int:
        """How many keys are strictly smaller than `key`."""
        raise NotImplementedError("implement Treap.rank")

    def to_list(self) -> list[Any]:
        raise NotImplementedError("implement Treap.to_list")

    def height(self) -> int:
        raise NotImplementedError("implement Treap.height")


class UnbalancedBST:
    """A plain BST, for contrast. Sorted insertion degenerates to a chain."""

    def __init__(self) -> None:
        raise NotImplementedError("implement UnbalancedBST.__init__")

    def insert(self, key: Any) -> None:
        raise NotImplementedError("implement UnbalancedBST.insert")

    def height(self) -> int:
        """Iterative on purpose - the interesting input is n deep."""
        raise NotImplementedError("implement UnbalancedBST.height")
