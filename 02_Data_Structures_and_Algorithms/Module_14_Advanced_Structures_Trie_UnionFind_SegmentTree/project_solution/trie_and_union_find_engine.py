"""Production solution for TrieAndUnionFindEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class TrieNode:
    __slots__ = ("children", "is_terminal")
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_terminal: bool = False

class PrefixTrie:
    """Prefix Tree with wildcard search and prefix validation."""

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_terminal = True

    def search(self, word: str) -> bool:
        curr = self.root
        for char in word:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return curr.is_terminal

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return True

    def wildcard_search(self, pattern: str) -> bool:
        """Search where '.' can match any valid transition."""
        def dfs(node: TrieNode, idx: int) -> bool:
            if idx == len(pattern):
                return node.is_terminal

            char = pattern[idx]
            if char == ".":
                return any(dfs(child, idx + 1) for child in node.children.values())
            else:
                if char not in node.children:
                    return False
                return dfs(node.children[char], idx + 1)

        return dfs(self.root, 0)


class DisjointSetUnion(Generic[T]):
    """Disjoint Set Union with path compression and rank heuristic."""

    def __init__(self) -> None:
        self.parent: dict[T, T] = {}
        self.rank: dict[T, int] = {}
        self._components: int = 0

    def add(self, x: T) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self._components += 1

    def find(self, x: T) -> T:
        if x not in self.parent:
            self.add(x)
            return x

        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: T, y: T) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self._components -= 1
        return True

    def connected(self, x: T, y: T) -> bool:
        return self.find(x) == self.find(y)

    def num_components(self) -> int:
        return self._components
