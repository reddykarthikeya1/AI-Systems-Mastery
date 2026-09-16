from __future__ import annotations

from radix_tree_cache import RadixTreeKVCache


def test_radix_prefix_cache_matching():
    cache = RadixTreeKVCache(max_cached_blocks=50)

    # Insert system prompt: tokens [1, 2, 3, 4] with blocks [101, 102]
    system_tokens = [1, 2, 3, 4]
    cache.insert(system_tokens, [101, 102])

    # Request 1: identical system prompt + user question [5, 6]
    matched_len, blocks = cache.match_prefix([1, 2, 3, 4, 5, 6])
    assert matched_len == 4
    assert blocks == [101, 102]


def test_unmatched_prefix_returns_zero():
    cache = RadixTreeKVCache(max_cached_blocks=50)
    cache.insert([10, 20, 30], [201])

    # Distinct leading token
    matched_len, blocks = cache.match_prefix([99, 10, 20])
    assert matched_len == 0
    assert len(blocks) == 0
