"""Problem 01 — Lru Cdn Cache Purge

Topic: 03 Edge Infrastructure Reverse Proxies
Target: Production-grade implementation

Purge cache entries matching tag or key prefix from edge dictionary.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def lru_cdn_cache_purge(cache: dict[str, dict], purge_tag: str) -> tuple[dict[str, dict], int]:
    """Each cache entry has format: key -> {'data': str, 'tags': list[str]}.
    Purge all entries whose 'tags' contains purge_tag.
    Returns (updated_cache, purged_count).
    """
    raise NotImplementedError("Implement lru_cdn_cache_purge")
