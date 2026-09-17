"""Reference Solution — Problem 01: Lru Cdn Cache Purge

Topic: 03 Edge Infrastructure Reverse Proxies
"""

from __future__ import annotations


def lru_cdn_cache_purge(cache: dict[str, dict], purge_tag: str) -> tuple[dict[str, dict], int]:
    res = {}
    purged = 0
    for k, v in cache.items():
        if purge_tag in v.get('tags', []):
            purged += 1
        else:
            res[k] = v
    return (res, purged)
