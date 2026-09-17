"""Beginner playground for Module 20 - Performance Optimization: Profiling & Caching.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import functools
import time

# -------------------------------------------- 1. LRU Caching with functools.lru_cache
call_count = 0
@functools.lru_cache(maxsize=128)
def expensive_calculation(n):
    global call_count
    call_count += 1
    return n * n

res1 = expensive_calculation(10)
res2 = expensive_calculation(10)
assert res1 == 100
assert res2 == 100
assert call_count == 1
assert expensive_calculation.cache_info().hits == 1
print(f"LRU cache hit: computation executed {call_count} time(s).")

# -------------------------------------------- 2. Microbenchmarking Code Sections
t0 = time.perf_counter()
total = sum(i for i in range(10_000))
elapsed = time.perf_counter() - t0
assert total == 49995000
assert elapsed >= 0
print(f"Summed 10,000 numbers in {elapsed*1000:.4f} ms.")

# -------------------------------------------- 3. String Concatenation Optimization
parts = [f"item_{i}" for i in range(100)]
joined = ",".join(parts)
assert len(joined.split(",")) == 100
assert joined.startswith("item_0")
assert joined.endswith("item_99")
print(f"Joined {len(parts)} tokens cleanly with O(N) memory allocation.")

print()
print("All checks passed.")
