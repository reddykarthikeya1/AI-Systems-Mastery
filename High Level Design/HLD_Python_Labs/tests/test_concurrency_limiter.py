"""Tests for Little's Law & Adaptive Concurrency Limiters (Chapter 01)."""
import pytest
from ch01_scalability.concurrency_limiter import (
    LittlesLawEstimator,
    AIMDConcurrencyLimiter,
    VegasAdaptiveLimiter,
    ConcurrencyLimitExceeded,
)


def test_littles_law_estimator():
    estimator = LittlesLawEstimator(window_seconds=10.0)
    # Simulate 5 completions spaced by 0.2s each taking 0.05s
    base_time = 1000.0
    for i in range(5):
        estimator.record_completion(duration_seconds=0.05, now=base_time + i * 0.2)

    # In 0.8s span, 5 requests -> ~6.25 req/s. Latency = 0.05s
    lam = estimator.get_arrival_rate(now=base_time + 1.0)
    w = estimator.get_average_latency(now=base_time + 1.0)
    concurrency_l = estimator.estimate_concurrency(now=base_time + 1.0)

    assert lam > 0
    assert w == pytest.approx(0.05, rel=1e-3)
    assert concurrency_l == pytest.approx(lam * w, rel=1e-3)


def test_aimd_limiter_concurrency_rejection():
    limiter = AIMDConcurrencyLimiter(initial_limit=2.0, min_limit=1.0)

    # Acquire 2 slots
    ctx1 = limiter.acquire()
    ctx2 = limiter.acquire()
    assert limiter.in_flight == 2

    # 3rd acquire should fail
    with pytest.raises(ConcurrencyLimitExceeded):
        limiter.acquire()

    assert limiter.rejections == 1

    # Release 1 slot
    limiter.release(duration_seconds=0.01, success=True)
    assert limiter.in_flight == 1

    # Now acquire should succeed
    ctx3 = limiter.acquire()
    assert limiter.in_flight == 2

    limiter.release(duration_seconds=0.01, success=True)
    limiter.release(duration_seconds=0.01, success=True)
    assert limiter.in_flight == 0


def test_aimd_adaptation_under_and_over_slo():
    limiter = AIMDConcurrencyLimiter(
        initial_limit=10.0,
        min_limit=2.0,
        max_limit=20.0,
        slo_latency_ms=100.0,
        additive_increase=1.0,
        backoff_factor=0.5,
    )

    # Normal success under SLO -> Additive Increase (+1)
    limiter.acquire()
    limiter.release(duration_seconds=0.05, success=True)  # 50ms < 100ms
    assert limiter.limit == 11.0

    # SLO violation -> Multiplicative Decrease (* 0.5)
    limiter.acquire()
    limiter.release(duration_seconds=0.15, success=True)  # 150ms > 100ms
    assert limiter.limit == 5.5

    # Failure -> Multiplicative Decrease
    limiter.acquire()
    limiter.release(duration_seconds=0.02, success=False)
    assert limiter.limit == 2.75


def test_vegas_adaptive_limiter():
    limiter = VegasAdaptiveLimiter(
        initial_limit=10.0,
        min_limit=2.0,
        max_limit=50.0,
        slo_latency_ms=300.0,
        alpha=2.0,
        beta=5.0,
    )

    # Base low-load latency of 20ms
    for _ in range(5):
        limiter.acquire()
        limiter.release(duration_seconds=0.02, success=True)

    assert limiter.min_rtt_ms == pytest.approx(20.0, abs=1.0)
    # Under low queue, limit should expand
    assert limiter.limit >= 10.0

    # Sudden high latency triggering queue buildup and backoff
    for _ in range(10):
        limiter.acquire()
        limiter.release(duration_seconds=0.25, success=True)

    # Should throttle down due to queue buildup
    metrics = limiter.get_metrics()
    assert metrics.in_flight == 0
    assert metrics.completions >= 15
