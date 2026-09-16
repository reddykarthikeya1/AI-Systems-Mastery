#!/usr/bin/env python3
"""Module 20 - A two-tier cache engine: in-process LRU/TTL (L1) + Redis (L2).

Real caches are layered. L1 lives in your process: nanosecond reads, but wiped
on restart and not shared between workers. L2 is a network service: microsecond
reads, survives restarts, and is shared by every worker. You want both.

::

    get(key)
      |
      +-- L1 hit? --> return                      (~100 ns, no I/O)
      |
      +-- L2 hit? --> promote into L1, return     (~200 us, one round trip)
      |
      +-- miss   --> call loader, write BOTH      (whatever the source costs)

Three bugs this file fixes from the naive version
-------------------------------------------------
1. **A docstring that claimed "thread-safe" with no lock.** Two threads racing
   on ``OrderedDict.move_to_end`` during eviction can corrupt the ordering or
   raise ``KeyError``. Fixed with an ``RLock``.
2. **``time.time()`` for TTLs.** The wall clock can jump backwards (NTP
   correction, DST, manual change), which either expires the whole cache at once
   or makes entries immortal. TTL logic must use ``time.monotonic()``.
3. **No stampede protection.** When a hot key expires under load, every
   concurrent request calls the loader simultaneously. Fixed with single-flight.
"""

from __future__ import annotations

import contextlib
import functools
import json
import pickle
import threading
import time
from collections import OrderedDict
from collections.abc import Callable, Hashable
from dataclasses import dataclass, field
from typing import Any, Generic, Protocol, TypeVar

T = TypeVar("T")

# Sentinel distinguishing "cached value is None" from "not in cache".
# Using None for both is a real and common cache bug: a legitimately null
# result gets re-computed on every single request.
MISSING: Any = object()


# ===========================================================================
# Metrics
# ===========================================================================


@dataclass
class CacheStats:
    """Counters for the one number that matters: hit ratio."""

    l1_hits: int = 0
    l2_hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    loads: int = 0
    stampedes_prevented: int = 0

    @property
    def hits(self) -> int:
        return self.l1_hits + self.l2_hits

    @property
    def total(self) -> int:
        return self.hits + self.misses

    @property
    def hit_ratio(self) -> float:
        return self.hits / self.total if self.total else 0.0

    @property
    def l1_ratio(self) -> float:
        """Share of hits served without any network I/O."""
        return self.l1_hits / self.hits if self.hits else 0.0

    def as_dict(self) -> dict[str, float | int]:
        return {
            "l1_hits": self.l1_hits,
            "l2_hits": self.l2_hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
            "loads": self.loads,
            "stampedes_prevented": self.stampedes_prevented,
            "hit_ratio": round(self.hit_ratio, 4),
            "l1_ratio": round(self.l1_ratio, 4),
        }

    def reset(self) -> None:
        for name in (
            "l1_hits", "l2_hits", "misses", "evictions",
            "expirations", "loads", "stampedes_prevented",
        ):
            setattr(self, name, 0)


# ===========================================================================
# L1: in-process LRU with TTL
# ===========================================================================


@dataclass(slots=True)
class _Entry:
    value: Any
    expires_at: float  # monotonic deadline, NOT a wall-clock timestamp


class LRUCache(Generic[T]):
    """Thread-safe O(1) LRU cache with per-key TTL.

    ``OrderedDict`` gives O(1) ``move_to_end`` and O(1) ``popitem(last=False)``,
    which is what makes both the recency update and the eviction constant-time.
    A plain dict plus a sorted list would make eviction O(n log n).

    Every public method takes ``self._lock``. ``RLock`` rather than ``Lock``
    because ``set`` calls ``_evict_if_needed`` while already holding it.
    """

    def __init__(self, capacity: int = 128, default_ttl: float = 60.0) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        if default_ttl <= 0:
            raise ValueError("default_ttl must be > 0")
        self.capacity = capacity
        self.default_ttl = default_ttl
        self._data: OrderedDict[str, _Entry] = OrderedDict()
        self._lock = threading.RLock()
        self.stats = CacheStats()

    def __len__(self) -> int:
        with self._lock:
            return len(self._data)

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not MISSING

    def get(self, key: str) -> Any:
        """Return the cached value, or ``MISSING``.

        Returns MISSING rather than None so that a cached ``None`` is a hit.
        """
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                self.stats.misses += 1
                return MISSING
            if time.monotonic() >= entry.expires_at:
                del self._data[key]
                self.stats.expirations += 1
                self.stats.misses += 1
                return MISSING
            self._data.move_to_end(key)  # mark as most-recently-used
            self.stats.l1_hits += 1
            return entry.value

    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """Insert or refresh a key, evicting the least-recently-used if needed."""
        ttl = self.default_ttl if ttl is None else ttl
        if ttl <= 0:
            raise ValueError("ttl must be > 0")
        with self._lock:
            self._data[key] = _Entry(value=value, expires_at=time.monotonic() + ttl)
            self._data.move_to_end(key)
            self._evict_if_needed()

    def delete(self, key: str) -> bool:
        with self._lock:
            return self._data.pop(key, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._data.clear()

    def purge_expired(self) -> int:
        """Drop every expired entry. Returns how many were removed.

        Lazy expiry (in ``get``) means dead entries occupy capacity until they
        are next requested. A periodic purge keeps a large cache honest.
        """
        with self._lock:
            now = time.monotonic()
            dead = [k for k, e in self._data.items() if now >= e.expires_at]
            for key in dead:
                del self._data[key]
            self.stats.expirations += len(dead)
            return len(dead)

    def _evict_if_needed(self) -> None:
        # Caller must already hold the lock.
        while len(self._data) > self.capacity:
            self._data.popitem(last=False)  # index 0 == least recently used
            self.stats.evictions += 1


# ===========================================================================
# L2: a pluggable shared backend
# ===========================================================================


class L2Backend(Protocol):
    """The shared, out-of-process cache tier."""

    name: str

    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any, ttl: float) -> None: ...
    def delete(self, key: str) -> bool: ...
    def clear(self) -> None: ...
    def ping(self) -> bool: ...


class RedisBackend:
    """A real Redis L2 tier.

    Two details that matter in production:

    * **Serialisation.** Redis stores bytes. JSON is portable across languages
      and safe; pickle handles arbitrary Python objects but will execute code on
      load, so **never** unpickle from a Redis instance you do not fully trust.
      JSON is the default here for that reason.
    * **Key namespacing.** A shared Redis holds many applications. Always
      prefix, or you will collide with someone else's ``user:1``.
    """

    name = "redis"

    def __init__(
        self,
        url: str = "redis://localhost:6379/0",
        namespace: str = "m20cache",
        serializer: str = "json",
        socket_timeout: float = 0.5,
    ) -> None:
        if serializer not in {"json", "pickle"}:
            raise ValueError("serializer must be 'json' or 'pickle'")
        import redis

        self.namespace = namespace
        self.serializer = serializer
        self._client = redis.Redis.from_url(
            url,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_timeout,
        )

    def _key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    def _dumps(self, value: Any) -> bytes:
        if self.serializer == "json":
            return json.dumps(value).encode()
        return pickle.dumps(value)

    def _loads(self, raw: bytes) -> Any:
        if self.serializer == "json":
            return json.loads(raw.decode())
        return pickle.loads(raw)

    def ping(self) -> bool:
        try:
            return bool(self._client.ping())
        except Exception:
            return False

    def get(self, key: str) -> Any:
        try:
            raw = self._client.get(self._key(key))
        except Exception:
            # A cache is an optimisation. If L2 is down, report a miss and let
            # the loader run - never propagate the failure to the caller.
            return MISSING
        if raw is None:
            return MISSING
        try:
            return self._loads(raw)
        except Exception:
            return MISSING  # poisoned/incompatible entry: treat as absent

    def set(self, key: str, value: Any, ttl: float) -> None:
        with contextlib.suppress(Exception):
            # px takes milliseconds; Redis enforces the TTL server-side, which
            # is why L2 entries expire correctly even if this process dies.
            self._client.set(self._key(key), self._dumps(value), px=int(ttl * 1000))

    def delete(self, key: str) -> bool:
        try:
            return bool(self._client.delete(self._key(key)))
        except Exception:
            return False

    def clear(self) -> None:
        """Delete only this namespace's keys. Never `FLUSHDB` a shared server."""
        try:
            cursor = 0
            pattern = f"{self.namespace}:*"
            while True:
                cursor, keys = self._client.scan(cursor=cursor, match=pattern, count=500)
                if keys:
                    self._client.delete(*keys)
                if cursor == 0:
                    break
        except Exception:
            pass


class InMemoryL2Backend:
    """A dict-backed L2 stand-in so the tests run with no Redis server.

    Explicitly named as in-memory. It is a **test double**, not a distributed
    cache - it is not shared between processes and does not survive a restart.
    """

    name = "memory"

    def __init__(self) -> None:
        self._data: dict[str, tuple[Any, float]] = {}
        self._lock = threading.RLock()

    def ping(self) -> bool:
        return True

    def get(self, key: str) -> Any:
        with self._lock:
            found = self._data.get(key)
            if found is None:
                return MISSING
            value, deadline = found
            if time.monotonic() >= deadline:
                del self._data[key]
                return MISSING
            return value

    def set(self, key: str, value: Any, ttl: float) -> None:
        with self._lock:
            self._data[key] = (value, time.monotonic() + ttl)

    def delete(self, key: str) -> bool:
        with self._lock:
            return self._data.pop(key, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._data.clear()


def load_l2_backend(url: str = "redis://localhost:6379/0", **kwargs: Any) -> L2Backend:
    """Return a Redis backend when one is reachable, else the in-memory double."""
    try:
        backend = RedisBackend(url=url, **kwargs)
        if backend.ping():
            return backend
    except Exception:
        pass
    return InMemoryL2Backend()


# ===========================================================================
# The two-tier engine
# ===========================================================================


@dataclass
class _Flight:
    """Tracks one in-progress load so concurrent callers can wait on it."""

    event: threading.Event = field(default_factory=threading.Event)
    value: Any = MISSING
    error: BaseException | None = None


class TwoTierCache:
    """L1 in-process LRU + L2 shared backend, with single-flight loading.

    The **cache-aside** pattern: the cache never talks to your database. The
    caller supplies a ``loader``, and the cache decides whether to call it.
    """

    def __init__(
        self,
        l1_capacity: int = 128,
        l1_ttl: float = 30.0,
        l2_ttl: float = 300.0,
        l2: L2Backend | None = None,
    ) -> None:
        if l1_ttl > l2_ttl:
            raise ValueError("l1_ttl must be <= l2_ttl (the inner tier expires first)")
        self.l1: LRUCache[Any] = LRUCache(capacity=l1_capacity, default_ttl=l1_ttl)
        self.l2 = l2 if l2 is not None else load_l2_backend()
        self.l1_ttl = l1_ttl
        self.l2_ttl = l2_ttl
        self.stats = CacheStats()
        self._flights: dict[str, _Flight] = {}
        self._flight_lock = threading.Lock()

    # -- plain access ------------------------------------------------------

    def get(self, key: str) -> Any:
        """Read through L1 then L2. Returns ``MISSING`` if absent from both."""
        value = self.l1.get(key)
        if value is not MISSING:
            self.stats.l1_hits += 1
            return value

        value = self.l2.get(key)
        if value is not MISSING:
            self.stats.l2_hits += 1
            self.l1.set(key, value, ttl=self.l1_ttl)  # promote for next time
            return value

        self.stats.misses += 1
        return MISSING

    def set(self, key: str, value: Any) -> None:
        """Write to both tiers."""
        self.l1.set(key, value, ttl=self.l1_ttl)
        self.l2.set(key, value, ttl=self.l2_ttl)

    def delete(self, key: str) -> None:
        """Invalidate in both tiers.

        Note the ordering problem this cannot solve alone: other processes still
        hold the key in *their* L1 until it expires. That is why L1 TTLs are
        short - they bound your staleness window. Strong invalidation across
        workers needs a pub/sub broadcast (Tier 3 challenge).
        """
        self.l1.delete(key)
        self.l2.delete(key)

    def clear(self) -> None:
        self.l1.clear()
        self.l2.clear()

    # -- cache-aside with stampede protection ------------------------------

    def get_or_load(self, key: str, loader: Callable[[], Any]) -> Any:
        """Return the cached value, calling ``loader`` at most once per key.

        **Cache stampede** (a.k.a. dogpile): a hot key expires, 500 concurrent
        requests all miss, and all 500 hit the database at once - frequently
        taking it down. Single-flight fixes it: the first caller loads, the rest
        wait on an Event and receive the same result.
        """
        value = self.get(key)
        if value is not MISSING:
            return value

        with self._flight_lock:
            flight = self._flights.get(key)
            if flight is not None:
                leader = False
            else:
                flight = _Flight()
                self._flights[key] = flight
                leader = True

        if not leader:
            self.stats.stampedes_prevented += 1
            flight.event.wait(timeout=10.0)
            if flight.error is not None:
                raise flight.error
            return flight.value

        try:
            loaded = loader()
            self.stats.loads += 1
            self.set(key, loaded)
            flight.value = loaded
            return loaded
        except BaseException as exc:
            flight.error = exc
            raise
        finally:
            flight.event.set()
            with self._flight_lock:
                self._flights.pop(key, None)

    def report(self) -> dict[str, float | int | str]:
        combined = self.stats.as_dict()
        combined["l2_backend"] = self.l2.name
        combined["l1_size"] = len(self.l1)
        return combined


# ===========================================================================
# Decorator interface
# ===========================================================================


def make_key(*args: Hashable, **kwargs: Hashable) -> str:
    """Build a stable cache key from call arguments.

    ``repr`` of a dict is insertion-ordered, so ``f(a=1, b=2)`` and
    ``f(b=2, a=1)`` would otherwise produce different keys for the same call.
    Sorting the kwargs fixes that.
    """
    parts = [repr(a) for a in args]
    parts += [f"{k}={v!r}" for k, v in sorted(kwargs.items())]
    return "|".join(parts)


def cached(cache: TwoTierCache, ttl: float | None = None) -> Callable[..., Any]:
    """Memoise a function through a ``TwoTierCache``.

    Compare with ``functools.lru_cache``, which you should prefer when you do
    not need TTLs, sharing across processes, or metrics:

    | Need                    | ``lru_cache`` | ``TwoTierCache`` |
    |-------------------------|---------------|------------------|
    | zero dependencies       | yes           | no               |
    | per-entry TTL           | **no**        | yes              |
    | shared across workers   | **no**        | yes              |
    | survives restart        | **no**        | yes (L2)         |
    | hit/miss metrics        | basic         | detailed         |
    | stampede protection     | **no**        | yes              |
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = f"{fn.__module__}.{fn.__qualname__}({make_key(*args, **kwargs)})"
            return cache.get_or_load(key, lambda: fn(*args, **kwargs))

        wrapper.cache = cache  # type: ignore[attr-defined]
        wrapper.cache_clear = cache.clear  # type: ignore[attr-defined]
        return wrapper

    return decorator


# ===========================================================================
# Demo
# ===========================================================================


def main() -> None:
    print("=" * 72)
    print("   MODULE 20 - TWO-TIER CACHE ENGINE (L1 in-process + L2 shared)")
    print("=" * 72)

    cache = TwoTierCache(l1_capacity=3, l1_ttl=2.0, l2_ttl=30.0)
    print(f"\n  L2 backend : {cache.l2.name}")
    if cache.l2.name == "memory":
        print("  (no Redis reachable - start one with:  docker run -p 6379:6379 redis)")

    # ---- LRU eviction ----------------------------------------------------
    print("\n" + "-" * 72)
    print(" 1. O(1) LRU EVICTION (capacity 3)")
    print("-" * 72)
    l1 = LRUCache[str](capacity=3, default_ttl=30)
    for k in ("a", "b", "c"):
        l1.set(k, k.upper())
    l1.get("a")            # 'a' becomes most-recently-used, so 'b' is now oldest
    l1.set("d", "D")       # evicts 'b'
    print("\n  after get('a') then set('d'):")
    for k in ("a", "b", "c", "d"):
        hit = l1.get(k) is not MISSING
        print(f"    {k}: {'HIT ' if hit else 'MISS'}{'  <- evicted' if not hit else ''}")
    print(f"  evictions: {l1.stats.evictions}")

    # ---- TTL uses a monotonic clock --------------------------------------
    print("\n" + "-" * 72)
    print(" 2. TTL EXPIRY (monotonic clock, immune to NTP jumps)")
    print("-" * 72)
    short = LRUCache[str](capacity=8, default_ttl=0.2)
    short.set("temp", "value")
    print(f"\n  immediately  : {'HIT' if short.get('temp') is not MISSING else 'MISS'}")
    time.sleep(0.25)
    print(f"  after 250 ms : {'HIT' if short.get('temp') is not MISSING else 'MISS'}")
    print(f"  expirations  : {short.stats.expirations}")

    # ---- L1 promotion ----------------------------------------------------
    print("\n" + "-" * 72)
    print(" 3. TIER PROMOTION")
    print("-" * 72)
    cache.clear()
    cache.stats.reset()
    cache.set("user:42", {"name": "Ada", "role": "admin"})
    cache.l1.clear()  # simulate a process restart: L1 gone, L2 intact
    print(f"\n  after L1 wipe, get('user:42') -> {cache.get('user:42')}")
    print("  served from L2 and promoted back into L1")
    print("  same key again              -> L1 hit")
    cache.get("user:42")
    print(f"  stats: {cache.stats.as_dict()}")

    # ---- Stampede protection --------------------------------------------
    print("\n" + "-" * 72)
    print(" 4. CACHE STAMPEDE PREVENTION (single-flight)")
    print("-" * 72)
    cache.clear()
    cache.stats.reset()
    load_calls = 0
    load_lock = threading.Lock()

    def slow_loader() -> str:
        nonlocal load_calls
        with load_lock:
            load_calls += 1
        time.sleep(0.3)  # a slow database query
        return "expensive-result"

    threads = [
        threading.Thread(target=lambda: cache.get_or_load("hot:key", slow_loader))
        for _ in range(20)
    ]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start

    print("\n  20 concurrent requests for one expired hot key")
    print(f"  loader invocations   : {load_calls}   (without single-flight: 20)")
    print(f"  stampedes prevented  : {cache.stats.stampedes_prevented}")
    print(f"  total wall clock     : {elapsed * 1000:.0f} ms  (~300 ms = one load)")

    # ---- The decorator ---------------------------------------------------
    print("\n" + "-" * 72)
    print(" 5. @cached DECORATOR")
    print("-" * 72)
    dec_cache = TwoTierCache(l1_capacity=64, l1_ttl=5.0, l2_ttl=60.0)
    calls = 0

    @cached(dec_cache)
    def fibonacci(n: int) -> int:
        nonlocal calls
        calls += 1
        time.sleep(0.01)
        return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)

    t0 = time.perf_counter()
    result = fibonacci(22)
    cold = time.perf_counter() - t0
    t0 = time.perf_counter()
    fibonacci(22)
    warm = time.perf_counter() - t0

    print(f"\n  fib(22)      = {result}")
    print(f"  cold call    : {cold * 1000:8.2f} ms  ({calls} distinct computations)")
    print(f"  warm call    : {warm * 1000:8.2f} ms")
    print(f"  speedup      : {cold / warm:8.0f}x")
    print(f"\n  report: {dec_cache.report()}")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
