#!/usr/bin/env python3
"""Module 18: Cache-Aside Pattern with TTL Demonstration.

This script demonstrates caching frequently accessed data in an in-memory
cache store with Time-To-Live (TTL) expiration.
"""

from __future__ import annotations

import time


class CacheAsideStore:
    def __init__(self) -> None:
        # key -> (value, expire_timestamp)
        self.store: dict[str, tuple[str, float]] = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> str | None:
        if key in self.store:
            val, exp = self.store[key]
            if time.time() < exp:
                self.hits += 1
                return val
            # Expired
            del self.store[key]
        self.misses += 1
        return None

    def set(self, key: str, value: str, ttl_seconds: float = 60.0) -> None:
        self.store[key] = (value, time.time() + ttl_seconds)


def slow_database_fetch(item_id: int) -> str:
    time.sleep(0.05)  # Simulate DB latency
    return f"Product-Record-#{item_id}"


def get_product(item_id: int, cache: CacheAsideStore) -> str:
    key = f"product:{item_id}"
    cached = cache.get(key)
    if cached:
        return cached

    # Cache miss -> Fetch DB & populate cache
    data = slow_database_fetch(item_id)
    cache.set(key, data, ttl_seconds=2.0)
    return data


def main() -> None:
    print("=" * 60)
    print("  Cache-Aside Pattern & Latency Benchmarking Demo")
    print("=" * 60)

    cache = CacheAsideStore()

    # Request 1 (Cache MISS)
    t0 = time.perf_counter()
    r1 = get_product(42, cache)
    t1 = time.perf_counter()
    print(f"Request 1 (MISS): Value='{r1}', Time={(t1 - t0) * 1000:.2f}ms")

    # Request 2 (Cache HIT)
    t2 = time.perf_counter()
    r2 = get_product(42, cache)
    t3 = time.perf_counter()
    print(f"Request 2 (HIT) : Value='{r2}', Time={(t3 - t2) * 1000:.2f}ms")

    print(f"\nStats: Hits={cache.hits}, Misses={cache.misses}")


if __name__ == "__main__":
    main()
