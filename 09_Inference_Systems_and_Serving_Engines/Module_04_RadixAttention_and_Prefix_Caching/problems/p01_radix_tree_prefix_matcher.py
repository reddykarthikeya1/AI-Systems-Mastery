"""Problem 01 — Radix Tree Prefix Matcher

Topic: 04 RadixAttention and Prefix Caching
Target: Production-grade implementation

Find length of longest matching prefix between query token sequence and cached prefixes.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def radix_tree_prefix_matcher(cached_prefixes: list[list[int]], query_tokens: list[int]) -> tuple[int, int]:
    """Find the cached prefix with the longest matching prefix with query_tokens.
    Returns (best_prefix_index, matching_length).
    If no matches or empty, return (-1, 0).
    """
    raise NotImplementedError("Implement radix_tree_prefix_matcher")
