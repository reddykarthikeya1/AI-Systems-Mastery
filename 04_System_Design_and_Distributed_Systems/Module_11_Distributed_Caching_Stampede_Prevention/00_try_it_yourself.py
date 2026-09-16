"""Beginner playground for Module 11 - Distributed Caching and Stampede Prevention.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import random

# --------------------------- 1. Cache-aside, the pattern almost everyone uses
database_calls = {"count": 0}
cache = {}


def load_from_database(key):
    database_calls["count"] += 1
    return f"value for {key}"


def cache_aside(key):
    if key in cache:
        return cache[key]
    value = load_from_database(key)
    cache[key] = value
    return value


database_calls["count"] = 0
for _ in range(5_000):
    cache_aside("popular_key")
print(f"5,000 sequential requests -> {database_calls['count']} database call(s)")
assert database_calls["count"] == 1, "when requests are spread out, the cache works"


# ------------------------ 2. Now expire it while 5,000 requests are in flight
def concurrent_burst(handler, requests=5_000):
    cache.clear()
    database_calls["count"] = 0
    in_flight = [handler("popular_key", arrival=i) for i in range(requests)]
    return database_calls["count"], in_flight


def naive_handler(key, arrival):
    if key in cache:
        return cache[key]
    value = load_from_database(key)      # all 5,000 arrive here together
    if arrival == 4_999:
        cache[key] = value               # only the last one finishes in time
    return value


calls, _ = concurrent_burst(naive_handler)
print(f"5,000 concurrent requests -> {calls:,} database calls")
assert calls == 5_000, "the database took the full burst"
print("The cache did not fail. It was simply empty at the wrong moment.")


# ----------------------- 3. Single flight: one request fetches, the rest wait
locks = {}


def single_flight_handler(key, arrival):
    if key in cache:
        return cache[key]
    if key in locks:
        return locks[key]                # somebody else is already fetching
    locks[key] = "pending"
    value = load_from_database(key)
    cache[key] = value
    locks[key] = value
    return value


cache.clear()
locks.clear()
calls, _ = concurrent_burst(single_flight_handler)
print(f"5,000 concurrent requests with single-flight -> {calls} database call(s)")
assert calls == 1, "exactly one request did the work"


# --------------------------------- 4. And stop all the keys expiring together
random.seed(11)
BASE_TTL = 3_600


def expiry_second(jitter_fraction):
    spread = int(BASE_TTL * jitter_fraction)
    return BASE_TTL + random.randint(-spread, spread)


no_jitter = [expiry_second(0.0) for _ in range(10_000)]
with_jitter = [expiry_second(0.1) for _ in range(10_000)]

worst_no_jitter = max(no_jitter.count(t) for t in set(no_jitter))
worst_with_jitter = max(with_jitter.count(t) for t in set(with_jitter))

print(f"no jitter:   worst second expires {worst_no_jitter:,} keys")
print(f"10% jitter:  worst second expires {worst_with_jitter:,} keys")
assert worst_no_jitter == 10_000, "one second carries the whole load"
assert worst_with_jitter < 100, "spread across a 12-minute window"


print()
print("All checks passed.")
