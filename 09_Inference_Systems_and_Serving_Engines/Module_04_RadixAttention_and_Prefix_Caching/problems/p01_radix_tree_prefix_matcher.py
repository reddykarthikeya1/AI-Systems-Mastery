"""Problem 01 — Radix Tree Prefix Matcher

Topic: 04 RadixAttention and Prefix Caching
Target: Production-grade implementation

Find length of longest matching prefix between query token sequence and cached prefixes.

Example:
    >>> radix_tree_prefix_matcher([[101, 205, 303], [101, 205, 999], [555]], [101, 205, 303, 404])
    (0, 3)

Hints:
    Hint 1: Matching is purely positional — RadixAttention can only reuse a
        cached KV prefix that agrees with the query token-by-token from the
        very start, so stop comparing at the first mismatch.
    Hint 2: For each cached sequence, walk it against `query_tokens` in
        lockstep (e.g. with `zip`), counting equal tokens until the first
        disagreement, then keep the best `(index, matched_length)` seen so
        far across all cached prefixes.
    Hint 3: On a tie, the FIRST cached prefix to reach that length wins, so
        only update the best when a new match is strictly longer (`>`, not
        `>=`); `zip` already stops at the shorter sequence so no manual
        bounds checking is needed; and no match at all (or an empty
        `cached_prefixes`) must return `(-1, 0)`.
"""

from __future__ import annotations


def radix_tree_prefix_matcher(cached_prefixes: list[list[int]], query_tokens: list[int]) -> tuple[int, int]:
    """Find the cached prefix with the longest matching prefix with query_tokens.
    Returns (best_prefix_index, matching_length).
    If no matches or empty, return (-1, 0).
    """
    raise NotImplementedError("Implement radix_tree_prefix_matcher")
