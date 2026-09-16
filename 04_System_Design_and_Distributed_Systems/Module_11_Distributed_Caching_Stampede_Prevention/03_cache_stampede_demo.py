#!/usr/bin/env python3
"""Module 11 Demo: Live Cache Stampede (Dogpiling) vs Single-Flight Collapse."""

import concurrent.futures
import sys
import time
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from distributed_cache_guard import DistributedCacheGuard


def main() -> None:
    print("=" * 72)
    print("  MODULE 11: CACHE STAMPEDE (DOGPILING) VS SINGLE-FLIGHT DEFENSE")
    print("=" * 72)

    db_counter = {"hits": 0}

    def simulated_slow_database_query() -> dict[str, str]:
        db_counter["hits"] += 1
        time.sleep(0.08)  # 80ms latency querying PostgreSQL table
        return {"headline": "Breaking News: Distributed Systems Breakthrough!"}

    cache = DistributedCacheGuard()

    print("\nSimulating 30 concurrent users requesting the homepage banner at the exact")
    print("moment the cache expires (Stampede / Dogpiling event)...")

    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(cache.get, "homepage_banner", simulated_slow_database_query)
            for _ in range(30)
        ]
        _ = [f.result() for f in concurrent.futures.as_completed(futures)]
    total_time = time.perf_counter() - t0

    print(f"\n30 concurrent requests completed in {total_time:.3f}s")
    print(f"Total Database Hits: {db_counter['hits']}")
    print(f"Cache Statistics:    {cache.stats}")

    print("\n--- Why this matters in Production ---")
    print("Without Single-Flight / Mutex Locking:")
    print("  -> 30 threads would trigger 30 parallel DB connections.")
    print("  -> Under 10,000 QPS, 10,000 concurrent queries hit PostgreSQL simultaneously,")
    print("     saturating the connection pool and causing cascading service failure.")
    print("\nWith Single-Flight Protection:")
    print("  -> Thread #1 locks the key and executes the query.")
    print("  -> Threads #2 through #30 block and share Thread #1's result.")
    print("  -> Database was hit EXACTLY ONCE!")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
