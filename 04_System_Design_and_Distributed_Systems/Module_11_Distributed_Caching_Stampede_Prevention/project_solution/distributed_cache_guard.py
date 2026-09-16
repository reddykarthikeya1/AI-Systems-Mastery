#!/usr/bin/env python3
"""Module 11: In-Process Architectural Simulation Model: Distributed Cache Client with Stampede Protection.

Implements:
- Cache-Aside pattern with monotonic TTL
- Single-Flight Promise Deduplication (collapses N concurrent misses into 1 DB query)
- Probabilistic Early Expiration (XFetch algorithm)
- Negative Caching to prevent cache penetration
"""

from __future__ import annotations

import math
import random
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

T = TypeVar("T")

# Sentinel representing "explicitly absent / not found" for negative caching
NULL_SENTINEL: Any = object()


@dataclass
class CacheEntry:
    value: Any
    created_at: float
    ttl_seconds: float
    computation_delta: float = 0.0  # Time in seconds taken to compute/load the value

    @property
    def is_expired(self) -> bool:
        return (time.monotonic() - self.created_at) >= self.ttl_seconds

    @property
    def remaining_ttl(self) -> float:
        return max(0.0, self.ttl_seconds - (time.monotonic() - self.created_at))


class SingleFlightGroup:
    """Ensures that for a given key, only ONE execution is in-flight at any time.

    Concurrent requests for the same key block and share the single result.
    Equivalent to Go's `golang.org/x/sync/singleflight`.
    """

    class _Call:
        def __init__(self) -> None:
            self.event = threading.Event()
            self.result: Any = None
            self.error: Exception | None = None

    def __init__(self) -> None:
        self._calls: dict[str, SingleFlightGroup._Call] = {}
        self._lock = threading.Lock()

    def do(self, key: str, fn: Callable[[], T]) -> T:
        with self._lock:
            if key in self._calls:
                call = self._calls[key]
                first_caller = False
            else:
                call = self._Call()
                self._calls[key] = call
                first_caller = True

        if not first_caller:
            # Wait for the first caller to finish
            call.event.wait()
            if call.error is not None:
                raise call.error
            return call.result

        # First caller executes the workload
        try:
            call.result = fn()
            return call.result
        except Exception as exc:
            call.error = exc
            raise
        finally:
            with self._lock:
                self._calls.pop(key, None)
            call.event.set()


class DistributedCacheGuard:
    """Production-grade cache client with Stampede & Penetration guards."""

    def __init__(self, beta: float = 1.0) -> None:
        self.beta = beta  # Beta parameter for XFetch probabilistic early refresh
        self._store: dict[str, CacheEntry] = {}
        self._single_flight = SingleFlightGroup()
        self._lock = threading.RLock()
        self.stats = {"hits": 0, "misses": 0, "db_loads": 0}

    def get(
        self,
        key: str,
        loader: Callable[[], T],
        ttl_seconds: float = 60.0,
        negative_ttl: float = 5.0,
    ) -> T | None:
        """Retrieves value from cache; on miss or XFetch trigger, loads via loader."""
        with self._lock:
            entry = self._store.get(key)

        # Check if cached and not expired
        if entry is not None and not entry.is_expired:
            # Probabilistic early expiration (XFetch algorithm)
            # Prevents stampede by triggering background refresh before hard expiry
            # Formula: remaining_ttl <= -beta * delta * ln(random(0,1))
            if self._should_early_refresh(entry):
                # Run single-flight refresh
                return self._load_via_single_flight(key, loader, ttl_seconds, negative_ttl)

            self.stats["hits"] += 1
            return None if entry.value is NULL_SENTINEL else entry.value

        self.stats["misses"] += 1
        return self._load_via_single_flight(key, loader, ttl_seconds, negative_ttl)

    def _should_early_refresh(self, entry: CacheEntry) -> bool:
        if entry.computation_delta <= 0:
            return False
        rnd = random.random()
        if rnd <= 0:
            return False
        # XFetch threshold
        threshold = -self.beta * entry.computation_delta * math.log(rnd)
        return entry.remaining_ttl <= threshold

    def _load_via_single_flight(
        self,
        key: str,
        loader: Callable[[], T],
        ttl_seconds: float,
        negative_ttl: float,
    ) -> T | None:
        def compute_wrapper() -> T | None:
            self.stats["db_loads"] += 1
            t0 = time.monotonic()
            val = loader()
            delta = time.monotonic() - t0

            with self._lock:
                if val is None:
                    # Negative Caching: prevent repeated penetration of non-existent keys
                    self._store[key] = CacheEntry(
                        value=NULL_SENTINEL,
                        created_at=time.monotonic(),
                        ttl_seconds=negative_ttl,
                        computation_delta=delta,
                    )
                else:
                    self._store[key] = CacheEntry(
                        value=val,
                        created_at=time.monotonic(),
                        ttl_seconds=ttl_seconds,
                        computation_delta=delta,
                    )
            return val

        return self._single_flight.do(key, compute_wrapper)

    def invalidate(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)
