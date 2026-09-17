"""Reference Solution — Problem 01: Radix Tree Prefix Matcher

Topic: 04 RadixAttention and Prefix Caching
"""

from __future__ import annotations


def radix_tree_prefix_matcher(cached_prefixes: list[list[int]], query_tokens: list[int]) -> tuple[int, int]:
    best_idx = -1
    best_len = 0
    for i, pref in enumerate(cached_prefixes):
        matched = 0
        for t1, t2 in zip(pref, query_tokens):
            if t1 == t2:
                matched += 1
            else:
                break
        if matched > best_len:
            best_len = matched
            best_idx = i
    return (best_idx, best_len)
