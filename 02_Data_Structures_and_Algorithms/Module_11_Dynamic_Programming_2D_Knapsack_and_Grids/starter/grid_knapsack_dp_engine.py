"""Starter template for GridKnapsackDPEngine."""
from __future__ import annotations


class GridKnapsackDPEngine:
    """2D dynamic programming algorithms."""

    @staticmethod
    def knapsack_01(weights: list[int], values: list[int], capacity: int) -> tuple[int, list[int]]:
        """0/1 Knapsack: return (max_value, indices_of_selected_items)."""
        raise NotImplementedError

    @staticmethod
    def longest_common_subsequence(text1: str, text2: str) -> int:
        """LCS length with O(min(N, M)) space optimization."""
        raise NotImplementedError

    @staticmethod
    def edit_distance(word1: str, word2: str) -> int:
        """Levenshtein distance between word1 and word2."""
        raise NotImplementedError
