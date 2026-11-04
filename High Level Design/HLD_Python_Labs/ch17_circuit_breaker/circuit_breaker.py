"""Thread-Safe Circuit Breaker with Atomic Single-Probe HALF_OPEN Protection.

The Half-Open Thundering Herd Flaw:
-----------------------------------
In naive circuit breakers, once the OPEN state timeout expires, state switches to
HALF_OPEN. If 1,000 concurrent requests arrive at that microsecond, all 1,000 pass
through simultaneously, immediately overwhelming the recovering service before the
first response even returns!

The Fix:
--------
Enforce an atomic single-probe admission guarantee:
1. When cooldown expires, exactly ONE thread is granted permission to probe the downstream service.
2. `probe_in_flight` flag is atomically asserted under mutex.
3. Any other concurrent request arriving while the probe is executing is rejected immediately
   with `CircuitBreakerProbeInFlightException` (or fast-fails like standard OPEN).
4. If the probe succeeds (up to `success_threshold` consecutive successes), breaker closes.
5. If the probe fails, breaker returns to OPEN with exponential backoff and jitter.
"""

from __future__ import annotations
import asyncio
import enum
import functools
import random
import threading
import time
from typing import Any, Callable, Optional


class CircuitState(str, enum.Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpenException(Exception):
    """Raised when call is rejected because breaker is OPEN."""


class CircuitBreakerProbeInFlightException(CircuitBreakerOpenException):
    """Raised when call is rejected because HALF_OPEN single probe is currently executing."""


class CircuitBreaker:
    """Production-grade Circuit Breaker with atomic single-probe concurrency protection."""

    def __init__(
        self,
        name: str = "default",
        failure_threshold: int = 5,
        success_threshold: int = 2,
        base_cooldown_seconds: float = 5.0,
        max_cooldown_seconds: float = 60.0,
        jitter: bool = True,
    ) -> None:
        self.name = name
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.base_cooldown_seconds = base_cooldown_seconds
        self.max_cooldown_seconds = max_cooldown_seconds
        self.jitter = jitter

        self._lock = threading.Lock()
        self._async_lock: Optional[asyncio.Lock] = None
        self._state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._half_open_successes = 0
        self._probe_in_flight = False
        self._cooldown_deadline: float = 0.0
        self._total_requests = 0
        self._total_rejections = 0

    @property
    def state(self) -> CircuitState:
        with self._lock:
            self._evaluate_state_under_lock(time.monotonic())
            return self._state

    def _get_async_lock(self) -> asyncio.Lock:
        if self._async_lock is None:
            self._async_lock = asyncio.Lock()
        return self._async_lock

    def _calculate_backoff(self) -> float:
        """Exponential backoff with full jitter: backoff = min(max_cd, base_cd * 2^(fail-1)) + jitter."""
        exponent = max(0, min(10, self._consecutive_failures - 1))
        backoff = min(self.max_cooldown_seconds, self.base_cooldown_seconds * (2 ** exponent))
        if self.jitter:
            backoff = backoff * (0.5 + random.random() * 0.5)
        return backoff

    def _evaluate_state_under_lock(self, now: float) -> None:
        """Internal state transition check (must be called with _lock held)."""
        if self._state == CircuitState.OPEN:
            if now >= self._cooldown_deadline:
                self._state = CircuitState.HALF_OPEN
                self._half_open_successes = 0
                self._probe_in_flight = False

    def pre_call(self) -> None:
        """Check circuit permission before executing the call.

        Enforces atomic single-probe admission in HALF_OPEN.
        """
        now = time.monotonic()
        with self._lock:
            self._total_requests += 1
            self._evaluate_state_under_lock(now)

            if self._state == CircuitState.OPEN:
                self._total_rejections += 1
                remaining = max(0.0, self._cooldown_deadline - now)
                raise CircuitBreakerOpenException(
                    f"Circuit '{self.name}' is OPEN. Retry in {remaining:.2f}s"
                )

            if self._state == CircuitState.HALF_OPEN:
                if self._probe_in_flight:
                    self._total_rejections += 1
                    raise CircuitBreakerProbeInFlightException(
                        f"Circuit '{self.name}' is HALF_OPEN and single probe is already in-flight."
                    )
                # Atomically claim the single probe slot
                self._probe_in_flight = True

    def post_call(self, success: bool) -> None:
        """Record the execution outcome and update state."""
        now = time.monotonic()
        with self._lock:
            if self._state == CircuitState.CLOSED:
                if success:
                    self._consecutive_failures = 0
                else:
                    self._consecutive_failures += 1
                    if self._consecutive_failures >= self.failure_threshold:
                        self._state = CircuitState.OPEN
                        backoff = self._calculate_backoff()
                        self._cooldown_deadline = now + backoff

            elif self._state == CircuitState.HALF_OPEN:
                self._probe_in_flight = False
                if success:
                    self._half_open_successes += 1
                    if self._half_open_successes >= self.success_threshold:
                        # Full recovery
                        self._state = CircuitState.CLOSED
                        self._consecutive_failures = 0
                        self._half_open_successes = 0
                else:
                    # Probe failed: Trip back to OPEN with escalated backoff
                    self._consecutive_failures += 1
                    self._state = CircuitState.OPEN
                    backoff = self._calculate_backoff()
                    self._cooldown_deadline = now + backoff

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Synchronously execute wrapped function protected by circuit breaker."""
        self.pre_call()
        try:
            result = func(*args, **kwargs)
            self.post_call(success=True)
            return result
        except Exception:
            self.post_call(success=False)
            raise

    async def call_async(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Asynchronously execute wrapped function protected by circuit breaker."""
        self.pre_call()
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            self.post_call(success=True)
            return result
        except Exception:
            self.post_call(success=False)
            raise

    def __enter__(self) -> CircuitBreaker:
        self.pre_call()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.post_call(success=(exc_type is None))

    def __call__(self, func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await self.call_async(func, *args, **kwargs)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return self.call(func, *args, **kwargs)
            return sync_wrapper
