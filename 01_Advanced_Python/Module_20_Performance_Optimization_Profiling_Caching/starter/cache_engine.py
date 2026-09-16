"""STARTER - Module 20: Performance Optimization Profiling Caching

Module 20 - A two-tier cache engine: in-process LRU/TTL (L1) + Redis (L2).

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_cache_engine.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/cache_engine.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
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
MISSING: Any = object()

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
        # [Tier 2] Algorithm: Implement CacheStats.hits adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement CacheStats.hits()")


    @property
    def total(self) -> int:
        # [Tier 2] Algorithm: Implement CacheStats.total adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement CacheStats.total()")


    @property
    def hit_ratio(self) -> float:
        # [Tier 2] Algorithm: Implement CacheStats.hit_ratio adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_hit_ratio_arithmetic
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement CacheStats.hit_ratio()")


    @property
    def l1_ratio(self) -> float:
        """Share of hits served without any network I/O."""
        # [Tier 2] Algorithm: Implement CacheStats.l1_ratio adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_hit_ratio_arithmetic
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement CacheStats.l1_ratio()")


    def as_dict(self) -> dict[str, float | int]:
        # [Tier 2] Algorithm: Implement CacheStats.as_dict adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement CacheStats.as_dict()")


    def reset(self) -> None:
        # [Tier 2] Algorithm: Implement CacheStats.reset adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_stats_reset
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement CacheStats.reset()")



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
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 20: implement LRUCache.__init__()")


    def __len__(self) -> int:
        # [Tier 2] Algorithm: Implement LRUCache.__len__ adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement LRUCache.__len__()")


    def __contains__(self, key: str) -> bool:
        # [Tier 2] Algorithm: Implement LRUCache.__contains__ adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_contains_respects_expiry
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement LRUCache.__contains__()")


    def get(self, key: str) -> Any:
        """Return the cached value, or ``MISSING``.

        Returns MISSING rather than None so that a cached ``None`` is a hit.

        """
        # [Tier 1] Algorithm: Implement LRUCache.get adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement LRUCache.get()")


    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """Insert or refresh a key, evicting the least-recently-used if needed."""
        # [Tier 2] Algorithm: Implement LRUCache.set adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement LRUCache.set()")


    def delete(self, key: str) -> bool:
        # [Tier 2] Algorithm: Implement LRUCache.delete adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_delete_and_clear
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement LRUCache.delete()")


    def clear(self) -> None:
        # [Tier 2] Algorithm: Implement LRUCache.clear adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_delete_and_clear
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement LRUCache.clear()")


    def purge_expired(self) -> int:
        """Drop every expired entry. Returns how many were removed.

        Lazy expiry (in ``get``) means dead entries occupy capacity until they
        are next requested. A periodic purge keeps a large cache honest.

        """
        # [Tier 2] Algorithm: Implement LRUCache.purge_expired adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_purge_expired_reclaims_capacity
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement LRUCache.purge_expired()")


    def _evict_if_needed(self) -> None:
        # [Tier 2] Algorithm: Implement LRUCache._evict_if_needed adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_lru_evicts_least_recently_used
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement LRUCache._evict_if_needed()")



class L2Backend(Protocol):
    """The shared, out-of-process cache tier."""
    name: str

    def get(self, key: str) -> Any:
        ...


    def set(self, key: str, value: Any, ttl: float) -> None:
        ...


    def delete(self, key: str) -> bool:
        ...


    def clear(self) -> None:
        ...


    def ping(self) -> bool:
        ...



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
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 20: implement RedisBackend.__init__()")


    def _key(self, key: str) -> str:
        # [Tier 2] Algorithm: Implement RedisBackend._key adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_missing_key_returns_sentinel_not_none
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement RedisBackend._key()")


    def _dumps(self, value: Any) -> bytes:
        # [Tier 2] Algorithm: Implement RedisBackend._dumps adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement RedisBackend._dumps()")


    def _loads(self, raw: bytes) -> Any:
        # [Tier 1] Algorithm: Normalize raw input data structure into typed
        #   domain representation.
        # HINTS:
        #  - Handle missing optional keys with sensible defaults (.get()
        #   pattern).
        #  - Coerce primitive data types safely and strip surrounding
        #   whitespace.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Watch for unexpected null or None values in optional fields.
        raise NotImplementedError("Module 20: implement RedisBackend._loads()")


    def ping(self) -> bool:
        # [Tier 2] Algorithm: Implement RedisBackend.ping adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement RedisBackend.ping()")


    def get(self, key: str) -> Any:
        # [Tier 1] Algorithm: Implement RedisBackend.get adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement RedisBackend.get()")


    def set(self, key: str, value: Any, ttl: float) -> None:
        # [Tier 2] Algorithm: Implement RedisBackend.set adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement RedisBackend.set()")


    def delete(self, key: str) -> bool:
        # [Tier 2] Algorithm: Implement RedisBackend.delete adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_delete_and_clear
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement RedisBackend.delete()")


    def clear(self) -> None:
        """Delete only this namespace's keys. Never `FLUSHDB` a shared server."""
        # [Tier 2] Algorithm: Implement RedisBackend.clear adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_delete_and_clear
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement RedisBackend.clear()")



class InMemoryL2Backend:
    """A dict-backed L2 stand-in so the tests run with no Redis server.

    Explicitly named as in-memory. It is a **test double**, not a distributed
    cache - it is not shared between processes and does not survive a restart.

    """
    name = "memory"

    def __init__(self) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 20: implement InMemoryL2Backend.__init__()")


    def ping(self) -> bool:
        # [Tier 2] Algorithm: Implement InMemoryL2Backend.ping adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement InMemoryL2Backend.ping()")


    def get(self, key: str) -> Any:
        # [Tier 1] Algorithm: Implement InMemoryL2Backend.get adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement InMemoryL2Backend.get()")


    def set(self, key: str, value: Any, ttl: float) -> None:
        # [Tier 2] Algorithm: Implement InMemoryL2Backend.set adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement InMemoryL2Backend.set()")


    def delete(self, key: str) -> bool:
        # [Tier 2] Algorithm: Implement InMemoryL2Backend.delete adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_delete_and_clear
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement InMemoryL2Backend.delete()")


    def clear(self) -> None:
        # [Tier 2] Algorithm: Implement InMemoryL2Backend.clear adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_delete_and_clear
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement InMemoryL2Backend.clear()")



def load_l2_backend(url: str = "redis://localhost:6379/0", **kwargs: Any) -> L2Backend:
    """Return a Redis backend when one is reachable, else the in-memory double."""
    # [Tier 1] Algorithm: Normalize raw input data structure into typed domain
    #   representation.
    # HINTS:
    #  - Handle missing optional keys with sensible defaults (.get() pattern).
    #  - Coerce primitive data types safely and strip surrounding whitespace.
    # GRADES: test_unreachable_redis_degrades_to_memory_backend
    # WARNING: Watch for unexpected null or None values in optional fields.
    raise NotImplementedError("Module 20: implement load_l2_backend()")


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
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 20: implement TwoTierCache.__init__()")


    def get(self, key: str) -> Any:
        """Read through L1 then L2. Returns ``MISSING`` if absent from both."""
        # [Tier 1] Algorithm: Implement TwoTierCache.get adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement TwoTierCache.get()")


    def set(self, key: str, value: Any) -> None:
        """Write to both tiers."""
        # [Tier 2] Algorithm: Implement TwoTierCache.set adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_set_then_get_returns_value
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement TwoTierCache.set()")


    def delete(self, key: str) -> None:
        """Invalidate in both tiers.

        Note the ordering problem this cannot solve alone: other processes still
        hold the key in *their* L1 until it expires. That is why L1 TTLs are
        short - they bound your staleness window. Strong invalidation across
        workers needs a pub/sub broadcast (Tier 3 challenge).

        """
        # [Tier 2] Algorithm: Implement TwoTierCache.delete adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_delete_and_clear
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement TwoTierCache.delete()")


    def clear(self) -> None:
        # [Tier 2] Algorithm: Implement TwoTierCache.clear adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_delete_and_clear
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement TwoTierCache.clear()")


    def get_or_load(self, key: str, loader: Callable[[], Any]) -> Any:
        """Return the cached value, calling ``loader`` at most once per key.

        **Cache stampede** (a.k.a. dogpile): a hot key expires, 500 concurrent
        requests all miss, and all 500 hit the database at once - frequently
        taking it down. Single-flight fixes it: the first caller loads, the rest
        wait on an Event and receive the same result.

        """
        # [Tier 1] Algorithm: Normalize raw input data structure into typed
        #   domain representation.
        # HINTS:
        #  - Handle missing optional keys with sensible defaults (.get()
        #   pattern).
        #  - Coerce primitive data types safely and strip surrounding
        #   whitespace.
        # GRADES: test_get_or_load_calls_loader_once
        # WARNING: Watch for unexpected null or None values in optional fields.
        raise NotImplementedError("Module 20: implement TwoTierCache.get_or_load()")


    def report(self) -> dict[str, float | int | str]:
        # [Tier 2] Algorithm: Implement TwoTierCache.report adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_l2_get_failure_reports_miss_not_exception
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 20: implement TwoTierCache.report()")



def make_key(*args: Hashable, **kwargs: Hashable) -> str:
    """Build a stable cache key from call arguments.

    ``repr`` of a dict is insertion-ordered, so ``f(a=1, b=2)`` and
    ``f(b=2, a=1)`` would otherwise produce different keys for the same call.
    Sorting the kwargs fixes that.

    """
    # [Tier 2] Algorithm: Implement make_key adhering to the contract defined in
    #   docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_make_key_is_kwarg_order_independent
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 20: implement make_key()")


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
    # [Tier 3] Algorithm: Implement cached adhering to the contract defined in
    #   docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_cached_none_is_a_hit_not_a_miss
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 20: implement cached()")


def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_set_then_get_returns_value
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 20: implement main()")


if __name__ == "__main__":
    main()
