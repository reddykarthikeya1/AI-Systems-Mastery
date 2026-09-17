"""Property and performance assertions for Distributed Caching & Stampede Prevention.

These complement the correctness tests in `test_distributed_cache_guard.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

import concurrent.futures
import time

import pytest
from distributed_cache_guard import DistributedCacheGuard


@pytest.mark.perf
@pytest.mark.slow
def test_a_cache_hit_is_dramatically_cheaper_than_the_loader() -> None:
    """A cache that is not faster than the thing it caches is not a cache."""
    cache = DistributedCacheGuard()

    def slow_loader() -> str:
        time.sleep(0.03)
        return "payload"

    t0 = time.perf_counter()
    cache.get("k", slow_loader, ttl_seconds=60.0)
    cold = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(200):
        cache.get("k", slow_loader, ttl_seconds=60.0)
    warm = (time.perf_counter() - t0) / 200

    assert cold / warm > 100, f"cache only {cold / warm:.0f}x faster than the loader"


@pytest.mark.perf
@pytest.mark.slow
@pytest.mark.concurrency
def test_single_flight_wall_clock_matches_one_load_not_n() -> None:
    """Beyond counting loader calls, the *elapsed time* must show collapsing.

    40 threads each wanting a 60 ms load should finish in roughly 60 ms, not
    2.4 seconds. If the waiters were serialised rather than sharing one result,
    this fails even when the call count looks right.
    """
    cache = DistributedCacheGuard()
    calls = {"n": 0}

    def loader() -> str:
        time.sleep(0.06)
        calls["n"] += 1
        return "value"

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as pool:
        results = [f.result() for f in
                   [pool.submit(cache.get, "hot", loader) for _ in range(40)]]
    elapsed = time.perf_counter() - start

    assert calls["n"] == 1, f"loader ran {calls['n']} times instead of once"
    assert all(r == "value" for r in results)
    assert elapsed < 0.06 * 6, (
        f"40 waiters took {elapsed * 1000:.0f} ms for a 60 ms load - "
        "they are being serialised, not sharing one flight."
    )


def test_expiry_triggers_exactly_one_reload() -> None:
    cache = DistributedCacheGuard()
    calls = {"n": 0}

    def loader() -> int:
        calls["n"] += 1
        return calls["n"]

    cache.get("k", loader, ttl_seconds=0.05)
    assert calls["n"] == 1
    time.sleep(0.08)
    cache.get("k", loader, ttl_seconds=0.05)
    assert calls["n"] == 2


def test_invalidate_forces_the_next_read_to_reload() -> None:
    cache = DistributedCacheGuard()
    calls = {"n": 0}

    def loader() -> int:
        calls["n"] += 1
        return calls["n"]

    cache.get("k", loader, ttl_seconds=60.0)
    cache.invalidate("k")
    cache.get("k", loader, ttl_seconds=60.0)
    assert calls["n"] == 2


def test_a_loader_raising_does_not_poison_the_key() -> None:
    """A failed load must be retryable, not cached as a permanent failure."""
    cache = DistributedCacheGuard()
    state = {"fail": True}

    def flaky() -> str:
        if state["fail"]:
            raise RuntimeError("upstream down")
        return "recovered"

    with pytest.raises(RuntimeError):
        cache.get("k", flaky, ttl_seconds=60.0)

    state["fail"] = False
    assert cache.get("k", flaky, ttl_seconds=60.0) == "recovered"


@pytest.mark.concurrency
def test_distinct_keys_do_not_block_each_other() -> None:
    """Single-flight must be per-key. A global lock would serialise everything."""
    cache = DistributedCacheGuard()

    def loader() -> str:
        time.sleep(0.05)
        return "v"

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(cache.get, f"key{i}", loader) for i in range(8)]
        [f.result() for f in futures]
    elapsed = time.perf_counter() - start

    assert elapsed < 0.05 * 4, (
        f"8 distinct keys took {elapsed * 1000:.0f} ms - the flight group is "
        "locking globally instead of per key."
    )
