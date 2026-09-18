"""Problem 01 — Lru Cdn Cache Purge

Topic: 03 Edge Infrastructure Reverse Proxies
Target: Production-grade implementation

Purge cache entries matching tag or key prefix from edge dictionary.

Example:
    >>> lru_cdn_cache_purge({'/a': {'data': 'A', 'tags': ['x']}, '/b': {'data': 'B', 'tags': ['y']}}, 'x')
    ({'/b': {'data': 'B', 'tags': ['y']}}, 1)

Hints:
    Hint 1: This is a filter over dict entries keyed by tag membership, not
        an in-place mutation -- entries whose tags do NOT contain the
        purge tag survive into the result.
    Hint 2: Build a fresh result dict by iterating `cache.items()`,
        checking whether `purge_tag` is in each entry's tag list, and
        counting how many entries you drop along the way.
    Hint 3: An entry missing the 'tags' key entirely must be treated as
        having no tags (so it is never purged) instead of raising a
        KeyError -- look up tags with `v.get('tags', [])`.
"""

from __future__ import annotations


def lru_cdn_cache_purge(cache: dict[str, dict], purge_tag: str) -> tuple[dict[str, dict], int]:
    """Each cache entry has format: key -> {'data': str, 'tags': list[str]}.
    Purge all entries whose 'tags' contains purge_tag.
    Returns (updated_cache, purged_count).
    """
    raise NotImplementedError("Implement lru_cdn_cache_purge")
