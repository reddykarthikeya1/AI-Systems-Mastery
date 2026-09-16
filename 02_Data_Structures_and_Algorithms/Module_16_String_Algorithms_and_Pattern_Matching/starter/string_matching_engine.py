"""Starter template for the string matching engine.

Implement each function. Run the shipped tests against your work:

    cd starter
    python -m pytest ../project_solution -q

They must FAIL until you have written the code. If they pass on this untouched
file, the grading loop is broken - report it.
"""
from __future__ import annotations

from typing import Any


def naive_search(text: str, pattern: str) -> list[int]:
    """Every starting offset where `pattern` occurs. O(n*m). Write this first -
    it is the reference your fast versions will be checked against."""
    raise NotImplementedError("implement naive_search")


def naive_search_char_by_char(text: str, pattern: str) -> list[int]:
    """The same algorithm with the inner comparison written out in Python.

    Exists so the timing tests can compare algorithm against algorithm rather
    than C against Python. Slice comparison is a C memcmp; this is not.
    """
    raise NotImplementedError("implement naive_search_char_by_char")


def prefix_function(pattern: str) -> list[int]:
    """pi[i] = length of the longest proper prefix of pattern[:i+1] that is
    also a suffix of it."""
    raise NotImplementedError("implement prefix_function")


def kmp_search(text: str, pattern: str) -> list[int]:
    """All occurrences, O(n + m), overlaps included."""
    raise NotImplementedError("implement kmp_search")


def smallest_period(word: str) -> int:
    """Length of the shortest string whose repetition builds `word`."""
    raise NotImplementedError("implement smallest_period")


def z_function(text: str) -> list[int]:
    """z[i] = longest substring starting at i that is also a prefix."""
    raise NotImplementedError("implement z_function")


def z_search(text: str, pattern: str, separator: str = "\x00") -> list[int]:
    """Find `pattern` using the Z-function over pattern + sep + text."""
    raise NotImplementedError("implement z_search")


class RollingHash:
    """Polynomial hash over a sliding window."""

    def __init__(self, window: int, base: int = 257, mod: int = (1 << 61) - 1) -> None:
        raise NotImplementedError("implement RollingHash.__init__")

    @classmethod
    def of(cls, text: str, base: int = 257, mod: int = (1 << 61) - 1) -> int:
        raise NotImplementedError("implement RollingHash.of")

    def push(self, character: str) -> int:
        raise NotImplementedError("implement RollingHash.push")

    def roll(self, outgoing: str, incoming: str) -> int:
        raise NotImplementedError("implement RollingHash.roll")


def rabin_karp_search(text: str, pattern: str) -> list[int]:
    """All occurrences, O(n + m) expected. Verify every hash match."""
    raise NotImplementedError("implement rabin_karp_search")


def rabin_karp_search_unverified(text: str, pattern: str, mod: int = 101) -> list[int]:
    """Deliberately trusts the hash. Keep the bug - a test asserts it."""
    raise NotImplementedError("implement rabin_karp_search_unverified")


def rabin_karp_2d(grid: list[str], pattern: list[str]) -> list[tuple[int, int]]:
    """Find a 2-D pattern block inside a 2-D grid."""
    raise NotImplementedError("implement rabin_karp_2d")


class AhoCorasick:
    """Match every pattern in a dictionary in one pass."""

    def __init__(self) -> None:
        raise NotImplementedError("implement AhoCorasick.__init__")

    def add(self, word: str) -> None:
        raise NotImplementedError("implement AhoCorasick.add")

    def build(self) -> Any:
        raise NotImplementedError("implement AhoCorasick.build")

    def search(self, text: str) -> list[tuple[int, str]]:
        raise NotImplementedError("implement AhoCorasick.search")

    def contains_any(self, text: str) -> bool:
        raise NotImplementedError("implement AhoCorasick.contains_any")


def build_automaton(patterns: list[str]) -> AhoCorasick:
    raise NotImplementedError("implement build_automaton")
