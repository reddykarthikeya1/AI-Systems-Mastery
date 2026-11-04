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

Production Hardening:
---------------------
1. Exception Classification:
   Only infrastructure/dependency errors (e.g. ConnectionError, TimeoutError, 5xx) count toward
   tripping the circuit breaker. Client errors (ValueError, KeyError, 4xx validation errors)
   are business faults, NOT dependency downtime, and must NOT trip the circuit.
2. asyncio.CancelledError Safety:
   Coroutine cancellation must NOT count as a dependency failure, and probe slot is released.
3. Call Timeout Protection:
   Both synchronous and asynchronous executions support strict request timeouts.
"""

from __future__ import annotations
import asyncio
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
import enum
import functools
import random
import threading
import time
from typing import Any, Callable, Optional, Tuple, Type


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
        call_timeout_seconds: Optional[float] = None,
        failure_exceptions: Optional[Tuple[Type[BaseException], ...]] = None,
        ignored_exceptions: Optional[Tuple[Type[BaseException], ...]] = None,
        failure_predicate: Optional[Callable[[BaseException], bool]] = None,
    ) -> None:
        if failure_threshold < 1:
            raise ValueError(f"failure_threshold must be >= 1, got {failure_threshold}")
        if success_threshold < 1:
            raise ValueError(f"success_threshold must be >= 1, got {success_threshold}")
        if base_cooldown_seconds <= 0:
            raise ValueError(f"base_cooldown_seconds must be > 0, got {base_cooldown_seconds}")
        if max_cooldown_seconds < base_cooldown_seconds:
            raise ValueError(
                f"max_cooldown_seconds ({max_cooldown_seconds}) must be >= base_cooldown_seconds ({base_cooldown_seconds})"
            )
        if call_timeout_seconds is not None and call_timeout_seconds <= 0:
            raise ValueError(f"call_timeout_seconds must be > 0, got {call_timeout_seconds}")

        self.name = name
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.base_cooldown_seconds = base_cooldown_seconds
        self.max_cooldown_seconds = max_cooldown_seconds
        self.jitter = jitter
        self.call_timeout_seconds = call_timeout_seconds
        self.failure_exceptions = failure_exceptions
        self.ignored_exceptions = ignored_exceptions
        self.failure_predicate = failure_predicate

        self._lock = threading.Lock()
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

    def is_dependency_failure(self, exc: BaseException) -> bool:
        """Determines whether an exception is classified as a downstream dependency failure."""
        if isinstance(exc, (asyncio.CancelledError, KeyboardInterrupt, SystemExit)):
            return False

        if self.failure_predicate is not None:
            return self.failure_predicate(exc)

        if self.ignored_exceptions and isinstance(exc, self.ignored_exceptions):
            return False

        if self.failure_exceptions is not None:
            return isinstance(exc, self.failure_exceptions)

        # Default classification: only infrastructure errors count as dependency failures
        return isinstance(exc, (ConnectionError, TimeoutError, OSError, FutureTimeoutError))

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

    def post_call(self, success: bool, exception: Optional[BaseException] = None) -> None:
        """Record the execution outcome and update state."""
        now = time.monotonic()
        with self._lock:
            # If an exception was provided, evaluate whether it is a real dependency failure
            if exception is not None and not success:
                if not self.is_dependency_failure(exception):
                    # Client or business logic error: do not penalize circuit breaker
                    if self._state == CircuitState.HALF_OPEN:
                        self._probe_in_flight = False
                    return

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

    def call(self, func: Callable, *args: Any, timeout: Optional[float] = None, **kwargs: Any) -> Any:
        """Synchronously execute wrapped function protected by circuit breaker."""
        self.pre_call()
        eff_timeout = timeout if timeout is not None else self.call_timeout_seconds

        if eff_timeout is not None and eff_timeout > 0:
            with ThreadPoolExecutor(max_workers=1) as executor:
                fut = executor.submit(func, *args, **kwargs)
                try:
                    result = fut.result(timeout=eff_timeout)
                    self.post_call(success=True)
                    return result
                except FutureTimeoutError as te:
                    timeout_exc = TimeoutError(f"Call exceeded timeout of {eff_timeout}s")
                    self.post_call(success=False, exception=timeout_exc)
                    raise timeout_exc from te
                except Exception as ex:
                    self.post_call(success=False, exception=ex)
                    raise
        else:
            try:
                result = func(*args, **kwargs)
                self.post_call(success=True)
                return result
            except Exception as ex:
                self.post_call(success=False, exception=ex)
                raise

    async def call_async(
        self, func: Callable, *args: Any, timeout: Optional[float] = None, **kwargs: Any
    ) -> Any:
        """Asynchronously execute wrapped function protected by circuit breaker."""
        self.pre_call()
        eff_timeout = timeout if timeout is not None else self.call_timeout_seconds

        try:
            if asyncio.iscoroutinefunction(func):
                coro = func(*args, **kwargs)
            else:
                coro = asyncio.to_thread(func, *args, **kwargs)

            if eff_timeout is not None and eff_timeout > 0:
                result = await asyncio.wait_for(coro, timeout=eff_timeout)
            else:
                result = await coro

            self.post_call(success=True)
            return result
        except asyncio.CancelledError:
            with self._lock:
                if self._state == CircuitState.HALF_OPEN:
                    self._probe_in_flight = False
            raise
        except asyncio.TimeoutError as te:
            timeout_exc = TimeoutError(f"Async call exceeded timeout of {eff_timeout}s")
            self.post_call(success=False, exception=timeout_exc)
            raise timeout_exc from te
        except Exception as ex:
            self.post_call(success=False, exception=ex)
            raise

    def __enter__(self) -> CircuitBreaker:
        self.pre_call()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        success = (exc_type is None)
        self.post_call(success=success, exception=exc_val)

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
