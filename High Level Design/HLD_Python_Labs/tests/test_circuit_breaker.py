"""Tests for Thread-Safe Circuit Breaker & HALF_OPEN Single-Probe Race Fix (Chapter 17)."""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
import pytest
from ch17_circuit_breaker.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
    CircuitBreakerOpenException,
    CircuitBreakerProbeInFlightException,
)


def test_circuit_breaker_normal_closed():
    cb = CircuitBreaker(failure_threshold=3)

    @cb
    def succeed():
        return "ok"

    assert succeed() == "ok"
    assert cb.state == CircuitState.CLOSED


def test_circuit_trips_to_open_on_failures():
    cb = CircuitBreaker(failure_threshold=2, base_cooldown_seconds=1.0, jitter=False)

    def failing():
        raise ConnectionError("Downstream timeout")

    # Failure 1
    with pytest.raises(ConnectionError):
        cb.call(failing)
    assert cb.state == CircuitState.CLOSED

    # Failure 2 reaches threshold -> trips to OPEN
    with pytest.raises(ConnectionError):
        cb.call(failing)
    assert cb.state == CircuitState.OPEN

    # Immediate next call must be fast-rejected without calling downstream
    with pytest.raises(CircuitBreakerOpenException):
        cb.call(failing)


def test_client_errors_do_not_trip_circuit():
    """Verify that client validation errors (e.g. ValueError, KeyError) do not trip the breaker."""
    cb = CircuitBreaker(failure_threshold=2, base_cooldown_seconds=1.0)

    def invalid_client_request():
        raise ValueError("Invalid user input: email format invalid")

    # Repeat 5 client errors (well over failure_threshold=2)
    for _ in range(5):
        with pytest.raises(ValueError):
            cb.call(invalid_client_request)

    # Circuit MUST remain CLOSED!
    assert cb.state == CircuitState.CLOSED
    assert cb._consecutive_failures == 0


def test_half_open_atomic_single_probe_race_fix():
    """Verifies that when OPEN cooldown expires:

    1. Exactly ONE probe is allowed through.
    2. Any concurrent request arriving while the probe is in flight is immediately rejected.
    """
    import threading

    cb = CircuitBreaker(
        failure_threshold=1,
        success_threshold=2,
        base_cooldown_seconds=10.0,
        jitter=False,
    )

    # Trip to OPEN
    with pytest.raises(ConnectionError):
        cb.call(lambda: (_ for _ in ()).throw(ConnectionError("trip")))
    assert cb.state == CircuitState.OPEN

    # Force cooldown expiration deterministically
    cb._cooldown_deadline = time.monotonic() - 1.0

    probe_started_event = threading.Event()
    probe_release_event = threading.Event()

    def slow_probe():
        try:
            cb.pre_call()
            probe_started_event.set()
            probe_release_event.wait(timeout=2.0)
            cb.post_call(success=True)
            return "probe_done"
        finally:
            probe_started_event.set()

    with ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(slow_probe)

        # Wait until thread 1 enters probe execution
        assert probe_started_event.wait(timeout=2.0) is True

        # Concurrently, thread 2 attempts to call while probe is in flight
        # Thread 2 MUST be rejected with CircuitBreakerProbeInFlightException!
        with pytest.raises(CircuitBreakerProbeInFlightException):
            cb.pre_call()

        # Let probe complete
        probe_release_event.set()
        res1 = f1.result(timeout=2.0)
        assert res1 == "probe_done"


def test_circuit_recovery_to_closed():
    cb = CircuitBreaker(
        failure_threshold=1,
        success_threshold=2,
        base_cooldown_seconds=0.03,
        jitter=False,
    )

    # Trip to OPEN
    with pytest.raises(ConnectionError):
        cb.call(lambda: (_ for _ in ()).throw(ConnectionError("fail")))
    assert cb.state == CircuitState.OPEN

    time.sleep(0.06)

    # 1st success in HALF_OPEN
    cb.call(lambda: "ok1")
    assert cb.state == CircuitState.HALF_OPEN

    # 2nd success meets success_threshold=2 -> Transitions back to CLOSED
    cb.call(lambda: "ok2")
    assert cb.state == CircuitState.CLOSED


def test_half_open_probe_failure_trips_to_open():
    """If the single probe in HALF_OPEN fails, breaker immediately trips back to OPEN."""
    cb = CircuitBreaker(
        failure_threshold=1,
        success_threshold=2,
        base_cooldown_seconds=0.03,
        jitter=False,
    )

    with pytest.raises(ConnectionError):
        cb.call(lambda: (_ for _ in ()).throw(ConnectionError("initial_fail")))
    assert cb.state == CircuitState.OPEN

    time.sleep(0.06)
    assert cb.state == CircuitState.HALF_OPEN

    # Probe fails
    with pytest.raises(ConnectionError):
        cb.call(lambda: (_ for _ in ()).throw(ConnectionError("probe_fail")))

    # Trips back to OPEN
    assert cb.state == CircuitState.OPEN


def test_call_timeout_synchronous():
    """Verify that synchronous calls exceeding timeout fail and trip the circuit."""
    cb = CircuitBreaker(failure_threshold=1, call_timeout_seconds=0.03)

    def slow_fn():
        time.sleep(0.1)
        return "slow_result"

    with pytest.raises(TimeoutError):
        cb.call(slow_fn)

    assert cb.state == CircuitState.OPEN


@pytest.mark.asyncio
async def test_async_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=2)

    @cb
    async def async_worker(x: int):
        return x * 2

    res = await async_worker(21)
    assert res == 42


@pytest.mark.asyncio
async def test_async_cancellation_does_not_trip_circuit():
    """Verify that cancelling an in-flight coroutine does not count as a dependency failure."""
    cb = CircuitBreaker(failure_threshold=1)

    async def long_running():
        await asyncio.sleep(1.0)
        return "ok"

    task = asyncio.create_task(cb.call_async(long_running))
    await asyncio.sleep(0.02)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    # Breaker must still be CLOSED!
    assert cb.state == CircuitState.CLOSED
    assert cb._consecutive_failures == 0


def test_parameter_validations():
    with pytest.raises(ValueError):
        CircuitBreaker(failure_threshold=0)
    with pytest.raises(ValueError):
        CircuitBreaker(success_threshold=0)
    with pytest.raises(ValueError):
        CircuitBreaker(base_cooldown_seconds=-1.0)
    with pytest.raises(ValueError):
        CircuitBreaker(base_cooldown_seconds=10.0, max_cooldown_seconds=5.0)
    with pytest.raises(ValueError):
        CircuitBreaker(call_timeout_seconds=0)
