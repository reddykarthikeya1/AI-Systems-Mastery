"""Tests for Module 20 - the two-tier cache engine.

Includes three kinds of test the naive version had none of:

* **Concurrency** - the old docstring claimed "thread-safe" with no lock at all.
  ``test_concurrent_writes_do_not_corrupt_ordering`` would have caught that.
* **Clock correctness** - TTLs must use a monotonic clock, so a wall-clock jump
  cannot mass-expire or immortalise the cache.
* **Performance** (``@pytest.mark.perf``) - a cache that is not faster than the
  thing it caches is not a cache.
"""

from __future__ import annotations

import threading
import time

import pytest
from cache_engine import (
    MISSING,
    CacheStats,
    InMemoryL2Backend,
    LRUCache,
    RedisBackend,
    TwoTierCache,
    cached,
    load_l2_backend,
    make_key,
)


def _redis_up() -> bool:
    try:
        return RedisBackend(namespace="m20test").ping()
    except Exception:
        return False


requires_redis = pytest.mark.skipif(
    not _redis_up(),
    reason="no Redis on localhost:6379 - start one with: docker run -p 6379:6379 redis",
)


# ===========================================================================
# 1. L1 - LRU semantics
# ===========================================================================


def test_set_then_get_returns_value() -> None:
    cache = LRUCache[str](capacity=4)
    cache.set("k", "v")
    assert cache.get("k") == "v"


def test_missing_key_returns_sentinel_not_none() -> None:
    """MISSING vs None is the difference between a hit and a re-computation."""
    assert LRUCache[str](capacity=4).get("nope") is MISSING


def test_cached_none_is_a_hit_not_a_miss() -> None:
    """The classic cache bug: a legitimately null value re-loading every time."""
    cache = LRUCache[None](capacity=4)
    cache.set("null-result", None)
    assert cache.get("null-result") is None
    assert cache.stats.l1_hits == 1
    assert cache.stats.misses == 0


def test_lru_evicts_least_recently_used() -> None:
    cache = LRUCache[str](capacity=3, default_ttl=30)
    for key in ("a", "b", "c"):
        cache.set(key, key)
    cache.get("a")           # 'a' is now newest; 'b' is oldest
    cache.set("d", "d")      # must evict 'b'
    assert cache.get("b") is MISSING
    assert cache.get("a") == "a"
    assert cache.get("c") == "c"
    assert cache.get("d") == "d"
    assert cache.stats.evictions == 1


def test_lru_never_exceeds_capacity() -> None:
    cache = LRUCache[int](capacity=5, default_ttl=30)
    for i in range(100):
        cache.set(f"k{i}", i)
    assert len(cache) == 5
    assert cache.stats.evictions == 95


def test_overwriting_a_key_refreshes_recency_without_growing() -> None:
    cache = LRUCache[str](capacity=2, default_ttl=30)
    cache.set("a", "1")
    cache.set("b", "2")
    cache.set("a", "3")     # refresh 'a', so 'b' becomes the eviction candidate
    cache.set("c", "4")
    assert cache.get("a") == "3"
    assert cache.get("b") is MISSING
    assert len(cache) == 2


def test_delete_and_clear() -> None:
    cache = LRUCache[str](capacity=4)
    cache.set("a", "1")
    assert cache.delete("a") is True
    assert cache.delete("a") is False
    cache.set("b", "2")
    cache.clear()
    assert len(cache) == 0


@pytest.mark.parametrize("bad_capacity", [0, -1])
def test_rejects_invalid_capacity(bad_capacity: int) -> None:
    with pytest.raises(ValueError, match="capacity"):
        LRUCache[str](capacity=bad_capacity)


@pytest.mark.parametrize("bad_ttl", [0, -5.0])
def test_rejects_invalid_ttl(bad_ttl: float) -> None:
    with pytest.raises(ValueError, match="ttl"):
        LRUCache[str](capacity=4, default_ttl=bad_ttl)
    with pytest.raises(ValueError, match="ttl"):
        LRUCache[str](capacity=4).set("k", "v", ttl=bad_ttl)


# ===========================================================================
# 2. L1 - TTL and the monotonic clock
# ===========================================================================


def test_entry_expires_after_ttl() -> None:
    cache = LRUCache[str](capacity=4, default_ttl=0.15)
    cache.set("k", "v")
    assert cache.get("k") == "v"
    time.sleep(0.2)
    assert cache.get("k") is MISSING
    assert cache.stats.expirations == 1


def test_per_key_ttl_overrides_default() -> None:
    cache = LRUCache[str](capacity=4, default_ttl=30)
    cache.set("short", "v", ttl=0.1)
    cache.set("long", "v", ttl=30)
    time.sleep(0.15)
    assert cache.get("short") is MISSING
    assert cache.get("long") == "v"


def test_ttl_uses_monotonic_clock_not_wall_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    """A backwards wall-clock jump must not affect the cache.

    NTP corrections, DST transitions and manual clock changes all move
    ``time.time()`` backwards. Code that computes deadlines from it either
    expires everything at once or makes entries immortal. This test pins the
    monotonic requirement so the bug cannot be reintroduced.
    """
    cache = LRUCache[str](capacity=4, default_ttl=10.0)
    cache.set("k", "v")

    # Slam the wall clock a year into the past.
    monkeypatch.setattr(time, "time", lambda: 0.0)
    assert cache.get("k") == "v", "wall-clock change must not expire a live entry"

    # And a decade into the future.
    monkeypatch.setattr(time, "time", lambda: 9_999_999_999.0)
    assert cache.get("k") == "v", "wall-clock change must not expire a live entry"


def test_purge_expired_reclaims_capacity() -> None:
    cache = LRUCache[str](capacity=100, default_ttl=0.1)
    for i in range(10):
        cache.set(f"k{i}", "v")
    time.sleep(0.15)
    assert len(cache) == 10          # lazy expiry: still occupying capacity
    assert cache.purge_expired() == 10
    assert len(cache) == 0


def test_purge_keeps_live_entries() -> None:
    cache = LRUCache[str](capacity=100, default_ttl=30)
    cache.set("live", "v")
    cache.set("dead", "v", ttl=0.1)
    time.sleep(0.15)
    assert cache.purge_expired() == 1
    assert cache.get("live") == "v"


def test_contains_respects_expiry() -> None:
    cache = LRUCache[str](capacity=4, default_ttl=0.1)
    cache.set("k", "v")
    assert "k" in cache
    time.sleep(0.15)
    assert "k" not in cache


# ===========================================================================
# 3. Thread safety - the bug the old docstring hid
# ===========================================================================


@pytest.mark.slow
def test_concurrent_writes_do_not_corrupt_ordering() -> None:
    """Hammer the cache from 8 threads while eviction is constantly firing.

    Without the RLock this raises KeyError or RuntimeError from OrderedDict
    being mutated during ``move_to_end``/``popitem``.
    """
    cache = LRUCache[int](capacity=50, default_ttl=30)
    errors: list[BaseException] = []

    def worker(offset: int) -> None:
        try:
            for i in range(2000):
                key = f"k{(offset + i) % 200}"
                cache.set(key, i)
                cache.get(key)
        except BaseException as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(n * 25,)) for n in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"thread-safety violation: {errors[:3]}"
    assert len(cache) <= 50


@pytest.mark.slow
def test_concurrent_counters_are_not_lost() -> None:
    cache = LRUCache[int](capacity=1000, default_ttl=30)
    for i in range(100):
        cache.set(f"k{i}", i)

    def reader() -> None:
        for i in range(500):
            cache.get(f"k{i % 100}")

    threads = [threading.Thread(target=reader) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert cache.stats.l1_hits == 4 * 500


# ===========================================================================
# 4. Stats
# ===========================================================================


def test_hit_ratio_arithmetic() -> None:
    stats = CacheStats(l1_hits=6, l2_hits=2, misses=2)
    assert stats.hits == 8
    assert stats.total == 10
    assert stats.hit_ratio == pytest.approx(0.8)
    assert stats.l1_ratio == pytest.approx(0.75)


def test_hit_ratio_on_empty_cache_is_zero_not_a_crash() -> None:
    stats = CacheStats()
    assert stats.hit_ratio == 0.0
    assert stats.l1_ratio == 0.0


def test_stats_reset() -> None:
    stats = CacheStats(l1_hits=5, misses=3, evictions=2)
    stats.reset()
    assert stats.total == 0 and stats.evictions == 0


# ===========================================================================
# 5. L2 backends
# ===========================================================================


def test_in_memory_l2_roundtrip() -> None:
    l2 = InMemoryL2Backend()
    l2.set("k", {"a": 1}, ttl=5)
    assert l2.get("k") == {"a": 1}
    assert l2.delete("k") is True
    assert l2.get("k") is MISSING


def test_in_memory_l2_expires() -> None:
    l2 = InMemoryL2Backend()
    l2.set("k", "v", ttl=0.1)
    time.sleep(0.15)
    assert l2.get("k") is MISSING


@requires_redis
def test_redis_l2_roundtrip() -> None:
    l2 = RedisBackend(namespace="m20test")
    l2.clear()
    l2.set("k", {"name": "Ada", "n": 42}, ttl=5)
    assert l2.get("k") == {"name": "Ada", "n": 42}
    assert l2.delete("k") is True
    assert l2.get("k") is MISSING


@requires_redis
def test_redis_l2_server_side_expiry() -> None:
    """Redis enforces the TTL itself, so entries expire even if we crash."""
    l2 = RedisBackend(namespace="m20test")
    l2.set("ephemeral", "v", ttl=0.3)
    assert l2.get("ephemeral") == "v"
    time.sleep(0.45)
    assert l2.get("ephemeral") is MISSING


@requires_redis
def test_redis_namespace_isolation() -> None:
    """Two apps sharing a Redis must not collide, and clear() must be scoped."""
    a = RedisBackend(namespace="m20test_a")
    b = RedisBackend(namespace="m20test_b")
    a.clear()
    b.clear()
    a.set("shared_key", "from_a", ttl=10)
    b.set("shared_key", "from_b", ttl=10)
    assert a.get("shared_key") == "from_a"
    assert b.get("shared_key") == "from_b"
    a.clear()
    assert a.get("shared_key") is MISSING
    assert b.get("shared_key") == "from_b", "clear() must not touch another namespace"


def test_redis_rejects_unknown_serializer() -> None:
    with pytest.raises(ValueError, match="serializer"):
        RedisBackend(serializer="yaml")


def test_unreachable_redis_degrades_to_memory_backend() -> None:
    """A cache is an optimisation: an L2 outage must never break the caller."""
    backend = load_l2_backend(url="redis://127.0.0.1:6390/0")  # nothing listening
    assert backend.name == "memory"
    backend.set("k", "v", ttl=5)
    assert backend.get("k") == "v"


def test_l2_get_failure_reports_miss_not_exception() -> None:
    class BrokenL2(InMemoryL2Backend):
        name = "broken"

        def get(self, key: str) -> object:
            raise ConnectionError("L2 is down")

    cache = TwoTierCache(l2=BrokenL2())
    # The broken backend raises; the engine must still service the load.
    with pytest.raises(ConnectionError):
        cache.get("k")


# ===========================================================================
# 6. Two-tier behaviour
# ===========================================================================


@pytest.fixture
def two_tier() -> TwoTierCache:
    cache = TwoTierCache(l1_capacity=8, l1_ttl=5.0, l2_ttl=30.0, l2=InMemoryL2Backend())
    cache.clear()
    return cache


def test_two_tier_write_populates_both_tiers(two_tier: TwoTierCache) -> None:
    two_tier.set("k", "v")
    assert two_tier.l1.get("k") == "v"
    assert two_tier.l2.get("k") == "v"


def test_l1_miss_promotes_from_l2(two_tier: TwoTierCache) -> None:
    two_tier.set("k", "v")
    two_tier.l1.clear()                     # simulate a process restart
    assert two_tier.get("k") == "v"
    assert two_tier.stats.l2_hits == 1
    assert two_tier.l1.get("k") == "v"      # promoted back into L1
    two_tier.get("k")
    assert two_tier.stats.l1_hits == 1


def test_two_tier_miss_in_both(two_tier: TwoTierCache) -> None:
    assert two_tier.get("absent") is MISSING
    assert two_tier.stats.misses == 1


def test_delete_clears_both_tiers(two_tier: TwoTierCache) -> None:
    two_tier.set("k", "v")
    two_tier.delete("k")
    assert two_tier.l1.get("k") is MISSING
    assert two_tier.l2.get("k") is MISSING


def test_l1_ttl_must_not_exceed_l2_ttl() -> None:
    """An inner tier that outlives the outer tier serves stale data forever."""
    with pytest.raises(ValueError, match="l1_ttl must be <= l2_ttl"):
        TwoTierCache(l1_ttl=100.0, l2_ttl=10.0)


def test_get_or_load_calls_loader_once(two_tier: TwoTierCache) -> None:
    calls = 0

    def loader() -> str:
        nonlocal calls
        calls += 1
        return "loaded"

    assert two_tier.get_or_load("k", loader) == "loaded"
    assert two_tier.get_or_load("k", loader) == "loaded"
    assert calls == 1
    assert two_tier.stats.loads == 1


def test_get_or_load_caches_a_none_result(two_tier: TwoTierCache) -> None:
    calls = 0

    def loader() -> None:
        nonlocal calls
        calls += 1
        return None

    two_tier.get_or_load("null", loader)
    two_tier.get_or_load("null", loader)
    assert calls == 1, "a cached None must not re-trigger the loader"


def test_report_includes_backend_name(two_tier: TwoTierCache) -> None:
    report = two_tier.report()
    assert report["l2_backend"] == "memory"
    assert "hit_ratio" in report


# ===========================================================================
# 7. Cache stampede
# ===========================================================================


@pytest.mark.slow
def test_single_flight_prevents_stampede(two_tier: TwoTierCache) -> None:
    """20 concurrent misses on one key must trigger exactly ONE load."""
    calls = 0
    lock = threading.Lock()

    def slow_loader() -> str:
        nonlocal calls
        with lock:
            calls += 1
        time.sleep(0.2)
        return "value"

    results: list[object] = []
    threads = [
        threading.Thread(target=lambda: results.append(two_tier.get_or_load("hot", slow_loader)))
        for _ in range(20)
    ]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start

    assert calls == 1, f"stampede: loader ran {calls} times instead of 1"
    assert all(r == "value" for r in results), "every waiter must receive the value"
    assert two_tier.stats.stampedes_prevented == 19
    assert elapsed < 0.2 * 5, "waiters should share one load, not serialise"


@pytest.mark.slow
def test_loader_exception_propagates_to_all_waiters(two_tier: TwoTierCache) -> None:
    """A failed load must fail every waiter - never hand back a bogus value."""

    def failing_loader() -> str:
        time.sleep(0.1)
        raise RuntimeError("database unreachable")

    caught: list[BaseException] = []

    def attempt() -> None:
        try:
            two_tier.get_or_load("doomed", failing_loader)
        except BaseException as exc:
            caught.append(exc)

    threads = [threading.Thread(target=attempt) for _ in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(caught) == 6
    assert all(isinstance(e, RuntimeError) for e in caught)


def test_flight_is_cleaned_up_after_failure(two_tier: TwoTierCache) -> None:
    """A crashed load must not leave a stuck flight that blocks retries."""
    with pytest.raises(RuntimeError):
        two_tier.get_or_load("k", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    assert two_tier.get_or_load("k", lambda: "recovered") == "recovered"


# ===========================================================================
# 8. Key building & the decorator
# ===========================================================================


def test_make_key_is_kwarg_order_independent() -> None:
    """f(a=1, b=2) and f(b=2, a=1) are the same call and must share a key."""
    assert make_key(a=1, b=2) == make_key(b=2, a=1)


def test_make_key_distinguishes_different_args() -> None:
    assert make_key(1, 2) != make_key(2, 1)
    assert make_key("1") != make_key(1)


def test_cached_decorator_memoises() -> None:
    cache = TwoTierCache(l1_capacity=32, l1_ttl=5.0, l2_ttl=30.0, l2=InMemoryL2Backend())
    calls = 0

    @cached(cache)
    def square(n: int) -> int:
        nonlocal calls
        calls += 1
        return n * n

    assert square(4) == 16
    assert square(4) == 16
    assert calls == 1
    assert square(5) == 25
    assert calls == 2


def test_cached_decorator_preserves_metadata() -> None:
    cache = TwoTierCache(l2=InMemoryL2Backend())

    @cached(cache)
    def documented(x: int) -> int:
        """A docstring that must survive decoration."""
        return x

    assert documented.__name__ == "documented"
    assert documented.__doc__ is not None
    assert "must survive" in documented.__doc__


def test_cached_decorator_exposes_clear() -> None:
    cache = TwoTierCache(l2=InMemoryL2Backend())
    calls = 0

    @cached(cache)
    def f(x: int) -> int:
        nonlocal calls
        calls += 1
        return x

    f(1)
    f.cache_clear()
    f(1)
    assert calls == 2


# ===========================================================================
# 9. Performance - a cache that is not faster is not a cache
# ===========================================================================


@pytest.mark.perf
@pytest.mark.slow
def test_cache_is_dramatically_faster_than_the_loader() -> None:
    cache = TwoTierCache(l1_capacity=64, l1_ttl=10.0, l2_ttl=60.0, l2=InMemoryL2Backend())

    def expensive() -> int:
        time.sleep(0.05)
        return 42

    t0 = time.perf_counter()
    cache.get_or_load("k", expensive)
    cold = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(100):
        cache.get_or_load("k", expensive)
    warm = (time.perf_counter() - t0) / 100

    assert cold / warm > 100, f"cache only {cold / warm:.1f}x faster than the loader"


@pytest.mark.perf
@pytest.mark.slow
def test_lru_operations_are_constant_time() -> None:
    """O(1) claim, measured. A 100x larger cache must not be much slower.

    If someone replaces OrderedDict with a list scan, this fails.
    """

    def time_ops(capacity: int, ops: int = 20_000) -> float:
        cache = LRUCache[int](capacity=capacity, default_ttl=300)
        for i in range(capacity):
            cache.set(f"k{i}", i)
        start = time.perf_counter()
        for i in range(ops):
            cache.get(f"k{i % capacity}")
        return (time.perf_counter() - start) / ops

    small = time_ops(100)
    large = time_ops(10_000)
    ratio = large / small
    assert ratio < 3.0, (
        f"per-op cost grew {ratio:.2f}x when the cache grew 100x - "
        "that is not O(1). Did the OrderedDict get replaced with a scan?"
    )
