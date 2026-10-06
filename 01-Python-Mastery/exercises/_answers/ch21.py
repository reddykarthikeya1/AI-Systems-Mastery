"""Chapter 21 - Scenario-based: Circuit breaker, LRU cache with TTL, and async event loop blocking.

1. CircuitBreaker: resilience pattern handling downstream RPC service failures.
2. LRUCacheTTL: thread-safe LRU cache with per-item time-to-live and capacity eviction.
3. fetch_metrics_async (debugging): fix event-loop stalling synchronous call in an async pipeline.
"""
import asyncio
import collections
import time


class CircuitBreakerOpenError(Exception):
    """Raised when an operation is attempted while the circuit breaker is OPEN."""
    pass


class CircuitBreaker:
    """State machine: CLOSED -> (failures >= threshold) -> OPEN -> (after timeout) -> HALF_OPEN -> CLOSED/OPEN."""
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 0.5):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_state_change = time.monotonic()

    def call(self, func, *args, **kwargs):
        now = time.monotonic()
        if self.state == "OPEN":
            if now - self.last_state_change > self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.last_state_change = now
            else:
                raise CircuitBreakerOpenError("Circuit is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                self.last_state_change = now
            elif self.state == "CLOSED":
                self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            if self.state in ("CLOSED", "HALF_OPEN") and self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_state_change = now
            elif self.state == "HALF_OPEN":
                self.state = "OPEN"
                self.last_state_change = now
            raise


class LRUCacheTTL:
    """LRU cache where keys expire after `ttl` seconds."""
    def __init__(self, maxsize: int = 100, default_ttl: float = 60.0):
        self.maxsize = maxsize
        self.default_ttl = default_ttl
        self._data = collections.OrderedDict()  # key -> (value, expiry_timestamp)

    def get(self, key, default=None):
        if key not in self._data:
            return default
        val, expiry = self._data[key]
        if time.monotonic() > expiry:
            del self._data[key]
            return default
        # Move to end for LRU recency
        self._data.move_to_end(key)
        return val

    def set(self, key, value, ttl=None):
        expiry = time.monotonic() + (ttl if ttl is not None else self.default_ttl)
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = (value, expiry)
        if len(self._data) > self.maxsize:
            self._data.popitem(last=False)  # Evict oldest

    def __len__(self):
        # Prune expired on length query
        now = time.monotonic()
        keys_to_del = [k for k, (_, exp) in self._data.items() if exp < now]
        for k in keys_to_del:
            del self._data[k]
        return len(self._data)


BUGGY = {
    "fetch_metrics_async": '''async def fetch_metrics_async(endpoints):
    """Fetch metrics for endpoints asynchronously."""
    results = []
    for ep in endpoints:
        # BUG: Synchronous time.sleep freezes the entire event loop!
        time.sleep(0.02)
        results.append(f"metrics:{ep}")
    return results''',
}


async def fetch_metrics_async(endpoints):
    """Fetch metrics for endpoints concurrently without stalling the event loop."""
    async def _fetch_one(ep):
        await asyncio.sleep(0.02)
        return f"metrics:{ep}"
    tasks = [_fetch_one(ep) for ep in endpoints]
    return await asyncio.gather(*tasks)


# --- Tests ---

def t_circuit_breaker_transitions(m):
    cb = m.CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
    
    def succeed():
        return "ok"
    
    def fail():
        raise RuntimeError("boom")

    assert cb.call(succeed) == "ok"
    assert cb.state == "CLOSED"
    
    # 1st failure
    try:
        cb.call(fail)
    except RuntimeError:
        pass
    assert cb.state == "CLOSED"
    
    # 2nd failure -> opens
    try:
        cb.call(fail)
    except RuntimeError:
        pass
    assert cb.state == "OPEN"
    
    # Immediate call blocked
    try:
        cb.call(succeed)
        assert False, "Should raise CircuitBreakerOpenError"
    except m.CircuitBreakerOpenError:
        pass

    # Wait for recovery timeout
    time.sleep(0.12)
    # Next call transitions to HALF_OPEN, succeeds, and resets to CLOSED
    assert cb.call(succeed) == "ok"
    assert cb.state == "CLOSED"


def t_lru_cache_ttl_eviction(m):
    cache = m.LRUCacheTTL(maxsize=2, default_ttl=0.1)
    cache.set("a", 1)
    cache.set("b", 2)
    assert cache.get("a") == 1
    # Adding 3rd evicts LRU ('b' because 'a' was accessed)
    cache.set("c", 3)
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3
    
    # Wait for TTL expiration
    time.sleep(0.12)
    assert cache.get("a") is None
    assert cache.get("c") is None


def t_fetch_metrics_async_concurrency(m):
    endpoints = [f"node-{i}" for i in range(5)]
    start = time.perf_counter()
    loop = asyncio.new_event_loop()
    try:
        res = loop.run_until_complete(m.fetch_metrics_async(endpoints))
    finally:
        loop.close()
    elapsed = time.perf_counter() - start
    assert len(res) == 5
    # Running 5 tasks of 0.02s concurrently must complete in < 0.08s (not 5 * 0.02 = 0.10s serialized)
    assert elapsed < 0.08, f"Took {elapsed:.3f}s: event loop was blocked!"
