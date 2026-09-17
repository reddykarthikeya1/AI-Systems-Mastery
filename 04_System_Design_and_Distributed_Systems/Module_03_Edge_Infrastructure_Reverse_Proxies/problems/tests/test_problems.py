"""Tests for Lru Cdn Cache Purge."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_lru_cdn_cache_purge import lru_cdn_cache_purge
except ImportError:
    from p01_lru_cdn_cache_purge import lru_cdn_cache_purge


def test_lru_cdn_cache_purge():
    cache = {
        "/item/1": {"data": "A", "tags": ["catalog", "apparel"]},
        "/item/2": {"data": "B", "tags": ["catalog", "electronics"]},
        "/news/1": {"data": "C", "tags": ["news"]}
    }
    updated, count = lru_cdn_cache_purge(cache, "apparel")
    assert count == 1
    assert "/item/1" not in updated
    assert len(updated) == 2
