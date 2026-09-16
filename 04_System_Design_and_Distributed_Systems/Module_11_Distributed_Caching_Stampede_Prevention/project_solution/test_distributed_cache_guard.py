"""Unit tests for Distributed Cache Guard and Stampede Prevention."""

from __future__ import annotations

import concurrent.futures
import time

from distributed_cache_guard import (
    DistributedCacheGuard,
)


def test_cache_hit_and_miss_lifecycle() -> None:
    cache = DistributedCacheGuard()
    db_reads = {"count": 0}

    def db_loader() -> str:
        db_reads["count"] += 1
        return "expensive_user_profile_data"

    # 1. First get: Cache Miss -> calls loader
    val1 = cache.get("user:101", db_loader, ttl_seconds=60.0)
    assert val1 == "expensive_user_profile_data"
    assert db_reads["count"] == 1
    assert cache.stats["hits"] == 0
    assert cache.stats["misses"] == 1

    # 2. Second get: Cache Hit -> does NOT call loader
    val2 = cache.get("user:101", db_loader, ttl_seconds=60.0)
    assert val2 == "expensive_user_profile_data"
    assert db_reads["count"] == 1
    assert cache.stats["hits"] == 1


def test_single_flight_collapses_stampede() -> None:
    """Core property: 50 concurrent requests for an expired key cause exactly 1 DB read."""
    cache = DistributedCacheGuard()
    db_reads = {"count": 0}

    def slow_db_loader() -> dict[str, int]:
        time.sleep(0.05)  # simulate 50ms database latency
        db_reads["count"] += 1
        return {"sku_1": 100}

    # Fire 50 threads simultaneously for the same key
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(cache.get, "hot_item_inventory", slow_db_loader) for _ in range(50)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    # All 50 threads received the correct data
    assert len(results) == 50
    for r in results:
        assert r == {"sku_1": 100}

    # Despite 50 concurrent requests, the database was hit EXACTLY ONCE!
    assert db_reads["count"] == 1
    assert cache.stats["db_loads"] == 1


def test_negative_caching_protects_penetration() -> None:
    cache = DistributedCacheGuard()
    db_reads = {"count": 0}

    def missing_db_loader() -> None:
        db_reads["count"] += 1
        return None  # record does not exist in DB

    # Request missing user: DB checked once
    res1 = cache.get("non_existent_user_999", missing_db_loader, ttl_seconds=60.0, negative_ttl=2.0)
    assert res1 is None
    assert db_reads["count"] == 1

    # Second request within negative_ttl returns None from cache without querying DB
    res2 = cache.get("non_existent_user_999", missing_db_loader, ttl_seconds=60.0, negative_ttl=2.0)
    assert res2 is None
    assert db_reads["count"] == 1
    assert cache.stats["hits"] == 1


def test_cache_invalidation() -> None:
    cache = DistributedCacheGuard()
    db_reads = {"count": 0}

    def loader() -> str:
        db_reads["count"] += 1
        return "v1"

    cache.get("key", loader)
    assert db_reads["count"] == 1

    # Invalidate key
    cache.invalidate("key")

    # Next get triggers reload
    cache.get("key", loader)
    assert db_reads["count"] == 2
