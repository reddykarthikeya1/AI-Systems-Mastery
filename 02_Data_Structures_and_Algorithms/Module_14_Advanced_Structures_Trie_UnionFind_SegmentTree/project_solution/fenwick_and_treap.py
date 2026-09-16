"""Fenwick trees and treaps - the two structures competitive programmers reach
for that rarely appear in an introductory course.

**Fenwick tree (Binary Indexed Tree).** Does exactly one job: point update and
prefix sum, both in O(log n). A segment tree does that too and much more, so why
does this exist? Because it is about four lines of code, uses a single flat
array with no nodes or recursion, and has a far smaller constant factor. When
the only thing you need is a running total under updates - and that is a
surprisingly common need: inversion counts, rank queries, "how many smaller
elements came before" - it is the right tool.

The trick is the indexing. `i & -i` isolates the lowest set bit of `i`, and the
tree stores at index `i` the sum of the `i & -i` elements ending at `i`. Every
prefix decomposes into O(log n) such blocks, one per set bit.

**Treap.** A binary search tree that stays balanced without any rebalancing
code. Each node gets a random priority, and the tree is kept a *heap* on
priority while remaining a *search tree* on key. Since the priorities are
random, the shape is the shape you would get by inserting in random order -
expected depth O(log n) - regardless of the order the keys actually arrive in.

Its real selling point is `split` and `merge`. Cutting a tree in two at a key,
or joining two trees, are both O(log n), and every other operation is written in
terms of them. That is what makes a treap the structure of choice when you need
to move whole ranges of a sequence around.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Fenwick tree
# ---------------------------------------------------------------------------


class FenwickTree:
    """Point update, prefix sum. One array, no nodes, no recursion.

    Indices in the public API are 0-based; internally the array is 1-based
    because the bit trick needs index 0 to be the terminator.
    """

    def __init__(self, size: int) -> None:
        if size < 0:
            raise ValueError("size must not be negative")
        self.size = size
        self.tree = [0] * (size + 1)

    @classmethod
    def from_values(cls, values: list[int]) -> FenwickTree:
        """Build in O(n) rather than n separate O(log n) updates.

        Each slot first holds its own value, then pushes its total into its
        parent. One pass, no logarithms.
        """
        tree = cls(len(values))
        for i, value in enumerate(values, start=1):
            tree.tree[i] += value
            parent = i + (i & -i)
            if parent <= tree.size:
                tree.tree[parent] += tree.tree[i]
        return tree

    def add(self, index: int, delta: int) -> None:
        """Add `delta` at position `index`. O(log n)."""
        if not 0 <= index < self.size:
            raise IndexError(f"index {index} out of range for size {self.size}")
        i = index + 1
        while i <= self.size:
            self.tree[i] += delta
            i += i & -i          # move to the next slot that covers this one

    def prefix_sum(self, count: int) -> int:
        """Sum of the first `count` elements, i.e. indices [0, count). O(log n)."""
        if count < 0 or count > self.size:
            raise IndexError(f"count {count} out of range for size {self.size}")
        total = 0
        i = count
        while i > 0:
            total += self.tree[i]
            i -= i & -i          # strip the lowest set bit
        return total

    def range_sum(self, start: int, stop: int) -> int:
        """Sum over the half-open interval [start, stop)."""
        if start > stop:
            raise IndexError("start must not exceed stop")
        return self.prefix_sum(stop) - self.prefix_sum(start)

    def find_kth(self, k: int) -> int:
        """Smallest index whose prefix sum is > k, when all values are counts.

        Binary lifting down the tree: O(log n), not O(log^2 n) from binary
        searching over `prefix_sum`. This is what turns a Fenwick tree into an
        order-statistic structure - "what is the k-th smallest element still in
        the multiset".
        """
        position = 0
        remaining = k
        step = 1 << (self.size.bit_length())
        while step:
            nxt = position + step
            if nxt <= self.size and self.tree[nxt] <= remaining:
                position = nxt
                remaining -= self.tree[nxt]
            step >>= 1
        return position          # 0-based index of the k-th item


def count_inversions(values: list[int]) -> int:
    """Pairs (i, j) with i < j and values[i] > values[j]. O(n log n).

    The classic Fenwick application. Sweep left to right over rank-compressed
    values, and for each element ask how many already-seen elements are larger.
    """
    order = {value: rank for rank, value in enumerate(sorted(set(values)))}
    tree = FenwickTree(len(order))
    inversions = 0
    for index, value in enumerate(values):
        rank = order[value]
        # Of the `index` elements already inserted, how many exceed this one?
        inversions += index - tree.prefix_sum(rank + 1)
        tree.add(rank, 1)
    return inversions


# ---------------------------------------------------------------------------
# Treap
# ---------------------------------------------------------------------------


@dataclass
class TreapNode:
    key: Any
    priority: float
    size: int = 1
    left: TreapNode | None = field(default=None)
    right: TreapNode | None = field(default=None)


def _size(node: TreapNode | None) -> int:
    return node.size if node else 0


def _update(node: TreapNode) -> TreapNode:
    node.size = 1 + _size(node.left) + _size(node.right)
    return node


def merge(low: TreapNode | None, high: TreapNode | None) -> TreapNode | None:
    """Join two treaps where every key in `low` is smaller than every key in
    `high`. The higher priority becomes the root, preserving the heap property.
    """
    if low is None:
        return high
    if high is None:
        return low
    if low.priority > high.priority:
        low.right = merge(low.right, high)
        return _update(low)
    high.left = merge(low, high.left)
    return _update(high)


def split(node: TreapNode | None, key: Any) -> tuple[TreapNode | None, TreapNode | None]:
    """Cut into (keys < key, keys >= key). O(log n) expected."""
    if node is None:
        return None, None
    if node.key < key:
        left, right = split(node.right, key)
        node.right = left
        return _update(node), right
    left, right = split(node.left, key)
    node.left = right
    return left, _update(node)


class Treap:
    """An ordered set with order statistics, balanced by randomness alone."""

    def __init__(self, seed: int | None = None) -> None:
        self.root: TreapNode | None = None
        self._random = random.Random(seed)

    def __len__(self) -> int:
        return _size(self.root)

    def __contains__(self, key: Any) -> bool:
        node = self.root
        while node:
            if node.key == key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def insert(self, key: Any) -> bool:
        """Insert unless already present. Returns True if the set changed."""
        if key in self:
            return False
        left, right = split(self.root, key)
        fresh = TreapNode(key=key, priority=self._random.random())
        self.root = merge(merge(left, fresh), right)
        return True

    def erase(self, key: Any) -> bool:
        """Remove a key. Returns True if it was there."""
        def drop(node: TreapNode | None) -> TreapNode | None:
            if node is None:
                return None
            if node.key == key:
                return merge(node.left, node.right)
            if key < node.key:
                node.left = drop(node.left)
            else:
                node.right = drop(node.right)
            return _update(node)

        if key not in self:
            return False
        self.root = drop(self.root)
        return True

    def kth(self, k: int) -> Any:
        """The k-th smallest key, 0-based. O(log n) expected.

        This is the operation a plain `set` cannot do at all - you would have to
        sort, which is O(n log n) every time you ask.
        """
        if not 0 <= k < len(self):
            raise IndexError(f"k={k} out of range for a treap of size {len(self)}")
        node = self.root
        while node:
            left_size = _size(node.left)
            if k == left_size:
                return node.key
            if k < left_size:
                node = node.left
            else:
                k -= left_size + 1
                node = node.right
        raise AssertionError("unreachable: sizes are inconsistent")

    def rank(self, key: Any) -> int:
        """How many keys are strictly smaller than `key`."""
        count = 0
        node = self.root
        while node:
            if key <= node.key:
                node = node.left
            else:
                count += _size(node.left) + 1
                node = node.right
        return count

    def to_list(self) -> list[Any]:
        out: list[Any] = []

        def walk(node: TreapNode | None) -> None:
            if node is None:
                return
            walk(node.left)
            out.append(node.key)
            walk(node.right)

        walk(self.root)
        return out

    def height(self) -> int:
        """Longest root-to-leaf path. Used by the tests to show that random
        priorities keep the tree shallow even on sorted input.
        """
        def deep(node: TreapNode | None) -> int:
            return 0 if node is None else 1 + max(deep(node.left), deep(node.right))

        return deep(self.root)


class UnbalancedBST:
    """A plain binary search tree, for contrast.

    Insert 1..n in order and this degenerates into a linked list of depth n.
    The treap, given the identical input, stays at roughly 2*log2(n). That
    comparison is the entire argument for randomised balancing, and a test
    measures it rather than asserting it.
    """

    def __init__(self) -> None:
        self.root: dict[str, Any] | None = None

    def insert(self, key: Any) -> None:
        fresh = {"key": key, "left": None, "right": None}
        if self.root is None:
            self.root = fresh
            return
        node = self.root
        while True:
            side = "left" if key < node["key"] else "right"
            if node[side] is None:
                node[side] = fresh
                return
            node = node[side]

    def height(self) -> int:
        # Iterative on purpose. The interesting input for this class is 1..n
        # inserted in order, which produces a chain n deep - and a recursive
        # height() would hit Python's recursion limit long before it returned.
        deepest = 0
        stack = [(self.root, 1)]
        while stack:
            node, depth = stack.pop()
            if node is None:
                continue
            deepest = max(deepest, depth)
            stack.append((node["left"], depth + 1))
            stack.append((node["right"], depth + 1))
        return deepest
