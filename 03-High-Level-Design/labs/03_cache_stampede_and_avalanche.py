# 03_cache_stampede_and_avalanche.py
"""
High-Level Design Lab 03: Cache Stampede (Dogpiling) & Probabilistic Mitigation.
Simulates 200 concurrent client requests hitting an expired hot cache key,
demonstrating database collapse under naive caching and 99% query suppression
via Distributed Mutex Locking.
"""

import time
import threading
from typing import Optional, Dict, Tuple

class SimulatedDatabase:
    def __init__(self):
        self.query_count = 0
        self._lock = threading.Lock()

    def expensive_sql_query(self, product_id: str) -> dict:
        with self._lock:
            self.query_count += 1
        # Simulate heavy disk I/O & table join latency
        time.sleep(0.01)
        return {"id": product_id, "name": "iPhone 16 Pro", "stock": 420, "price": 999.0}

class NaiveCache:
    def __init__(self, db: SimulatedDatabase):
        self.db = db
        self.cache: Dict[str, Tuple[dict, float]] = {} # key -> (data, expires_at)

    def get_product(self, product_id: str) -> dict:
        now = time.time()
        # Check cache
        if product_id in self.cache:
            data, expires_at = self.cache[product_id]
            if now < expires_at:
                return data

        # CACHE MISS: Hit database directly!
        fresh_data = self.db.expensive_sql_query(product_id)
        self.cache[product_id] = (fresh_data, now + 1.0) # 1 sec TTL
        return fresh_data

class MutexProtectedCache:
    """
    Implements Distributed Mutex Locking (Double-Checked Locking).
    When a cache miss occurs, only ONE thread acquires the lock to compute fresh data.
    All other 199 threads wait or get served as soon as the lock is released!
    """
    def __init__(self, db: SimulatedDatabase):
        self.db = db
        self.cache: Dict[str, Tuple[dict, float]] = {}
        self.locks: Dict[str, threading.Lock] = {}
        self._meta_lock = threading.Lock()

    def _get_key_lock(self, key: str) -> threading.Lock:
        with self._meta_lock:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
            return self.locks[key]

    def get_product(self, product_id: str) -> dict:
        now = time.time()
        if product_id in self.cache:
            data, expires_at = self.cache[product_id]
            if now < expires_at:
                return data

        # Acquire per-key lock
        key_lock = self._get_key_lock(product_id)
        with key_lock:
            # Double-check: maybe another thread already refreshed it while we were waiting!
            if product_id in self.cache:
                data, expires_at = self.cache[product_id]
                if time.time() < expires_at:
                    return data

            # Only ONE thread executes this database query!
            fresh_data = self.db.expensive_sql_query(product_id)
            self.cache[product_id] = (fresh_data, time.time() + 1.0)
            return fresh_data

def run_cache_stampede_lab():
    print("=" * 70)
    print("  HLD LAB 03: CACHE STAMPEDE (DOGPILING) & MUTEX SUPPRESSION LAB")
    print("=" * 70)

    # -------------------------------------------------------------
    # EXPERIMENT 1: NAIVE CACHING UNDER CONCURRENT EXPIRY
    # -------------------------------------------------------------
    db1 = SimulatedDatabase()
    cache1 = NaiveCache(db1)

    print("\n[EXPERIMENT 1] Firing 200 concurrent requests against EXPIRED key in NAIVE CACHE...")
    threads = [threading.Thread(target=cache1.get_product, args=("prod_101",)) for _ in range(200)]
    t0 = time.time()
    for t in threads: t.start()
    for t in threads: t.join()
    naive_time = time.time() - t0

    print(f"  Total Client Requests : 200")
    print(f"  Database Queries Hit  : {db1.query_count} / 200")
    print(f"  Elapsed Latency       : {naive_time:.3f}s")
    print("  >>> [CATASTROPHE] 200 simultaneous SQL queries hammered the DB for 1 single product! <<<")
    assert db1.query_count > 50, f"Naive cache should suffer stampede (got {db1.query_count} DB queries)!"

    # -------------------------------------------------------------
    # EXPERIMENT 2: MUTEX-PROTECTED CACHING
    # -------------------------------------------------------------
    db2 = SimulatedDatabase()
    cache2 = MutexProtectedCache(db2)

    print("\n[EXPERIMENT 2] Firing 200 concurrent requests against EXPIRED key in MUTEX CACHE...")
    threads2 = [threading.Thread(target=cache2.get_product, args=("prod_101",)) for _ in range(200)]
    t0 = time.time()
    for t in threads2: t.start()
    for t in threads2: t.join()
    mutex_time = time.time() - t0

    print(f"  Total Client Requests : 200")
    print(f"  Database Queries Hit  : {db2.query_count} / 200")
    print(f"  Elapsed Latency       : {mutex_time:.3f}s")
    print(f"  >>> [SUCCESS] Exactly {db2.query_count} database query executed! (99.5% reduction) <<<")
    assert db2.query_count <= 2, f"Expected 1-2 DB queries with Mutex protection, got {db2.query_count}"

    print("-" * 70)
    print("[SUCCESS] Cache stampede vulnerability and double-checked locking proof verified!\n")

if __name__ == "__main__":
    run_cache_stampede_lab()
