"""Tests for Thread-Safe Circuit Breaker & HALF_OPEN Single-Probe Race Fix (Chapter 17)."""
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
        raise ValueError("Downstream timeout")

    # Failure 1
    with pytest.raises(ValueError):
        cb.call(failing)
    assert cb.state == CircuitState.CLOSED

    # Failure 2 reaches threshold -> trips to OPEN
    with pytest.raises(ValueError):
        cb.call(failing)
    assert cb.state == CircuitState.OPEN

    # Immediate next call must be fast-rejected without calling downstream
    with pytest.raises(CircuitBreakerOpenException):
        cb.call(failing)


def test_half_open_atomic_single_probe_race_fix():
    """Verifies that when OPEN cooldown expires:

    1. Exactly ONE probe is allowed through.
    2. Any concurrent request arriving while the probe is in flight is immediately rejected.
    """
    import threading

    cb = CircuitBreaker(
        failure_threshold=1,
        success_threshold=2,
        base_cooldown_seconds=10.0,  # Long cooldown so it only expires when we force it
        jitter=False,
    )

    # Trip to OPEN
    with pytest.raises(RuntimeError):
        cb.call(lambda: (_ for _ in ()).throw(RuntimeError("trip")))
    assert cb.state == CircuitState.OPEN

    # Force cooldown expiration deterministically
    cb._cooldown_deadline = time.monotonic() - 1.0

    probe_started_event = threading.Event()
    probe_release_event = threading.Event()

    # Simulate thread 1 executing a probe in HALF_OPEN
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
        base_cooldown_seconds=0.02,
        jitter=False,
    )

    # Trip to OPEN
    with pytest.raises(Exception):
        cb.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    assert cb.state == CircuitState.OPEN

    time.sleep(0.03)

    # 1st success in HALF_OPEN
    cb.call(lambda: "ok1")
    assert cb.state == CircuitState.HALF_OPEN

    # 2nd success meets success_threshold=2 -> Transitions back to CLOSED
    cb.call(lambda: "ok2")
    assert cb.state == CircuitState.CLOSED


@pytest.mark.asyncio
async def test_async_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=2)

    @cb
    async def async_worker(x: int):
        return x * 2

    res = await async_worker(21)
    assert res == 42
