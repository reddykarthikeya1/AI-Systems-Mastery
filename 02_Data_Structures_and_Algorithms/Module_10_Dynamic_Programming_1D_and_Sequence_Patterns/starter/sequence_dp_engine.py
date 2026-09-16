"""Starter template for SequenceDPEngine."""
from __future__ import annotations


class SequenceDPEngine:
    """1D sequence dynamic programming algorithms."""

    @staticmethod
    def longest_increasing_subsequence(nums: list[int]) -> tuple[int, list[int]]:
        """Compute length and reconstructed LIS in O(N log N) time."""
        raise NotImplementedError

    @staticmethod
    def coin_change_min_coins(coins: list[int], amount: int) -> tuple[int, list[int]]:
        """Compute min coins needed to make amount, and reconstructed coin list. Returns (-1, []) if impossible."""
        raise NotImplementedError

    @staticmethod
    def word_break(s: str, word_dict: list[str]) -> bool:
        """Determine if string can be segmented into dictionary words."""
        raise NotImplementedError
