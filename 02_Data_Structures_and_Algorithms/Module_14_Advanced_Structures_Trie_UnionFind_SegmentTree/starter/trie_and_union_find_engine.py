"""Starter template for TrieAndUnionFindEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_terminal: bool = False

class PrefixTrie:
    """Prefix Tree supporting exact search, prefix lookup, and wildcard query."""
    def __init__(self) -> None:
        raise NotImplementedError

    def insert(self, word: str) -> None:
        raise NotImplementedError

    def search(self, word: str) -> bool:
        raise NotImplementedError

    def starts_with(self, prefix: str) -> bool:
        raise NotImplementedError

    def wildcard_search(self, pattern: str) -> bool:
        """Search where '.' matches any single character."""
        raise NotImplementedError

class DisjointSetUnion(Generic[T]):
    """DSU with path compression and union by rank."""
    def __init__(self) -> None:
        raise NotImplementedError

    def find(self, x: T) -> T:
        raise NotImplementedError

    def union(self, x: T, y: T) -> bool:
        raise NotImplementedError

    def connected(self, x: T, y: T) -> bool:
        raise NotImplementedError

    def num_components(self) -> int:
        raise NotImplementedError
