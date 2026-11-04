"""Tests for Dual-Dimensional Token Bucket Limiter (RPM + TPM) (Chapter 15)."""
import pytest
from ch15_rate_limiter.dual_token_bucket import DualTokenBucketLimiter


def test_dual_token_bucket_normal_acquisition():
    limiter = DualTokenBucketLimiter(max_rpm=60.0, max_tpm=1000.0)
    now = 1000.0

    # Acquire 1 request with 100 tokens
    res = limiter.acquire("tenant_1", tokens_requested=100, now=now)
    assert res.allowed is True
    assert res.remaining_rpm == pytest.approx(59.0)
    assert res.remaining_tpm == pytest.approx(900.0)
    assert res.retry_after_seconds == 0.0


def test_rpm_exhaustion():
    limiter = DualTokenBucketLimiter(max_rpm=2.0, max_tpm=1000.0)
    now = 1000.0

    res1 = limiter.acquire("client_A", tokens_requested=10, now=now)
    assert res1.allowed is True

    res2 = limiter.acquire("client_A", tokens_requested=10, now=now)
    assert res2.allowed is True

    # 3rd request in same second exceeds RPM (2.0)
    res3 = limiter.acquire("client_A", tokens_requested=10, now=now)
    assert res3.allowed is False
    assert res3.reason == "RPM Exceeded"
    assert res3.retry_after_seconds > 0.0


def test_tpm_exhaustion_atomic_rollback():
    limiter = DualTokenBucketLimiter(max_rpm=10.0, max_tpm=100.0)
    now = 1000.0

    # Request 150 tokens when TPM capacity is 100
    res = limiter.acquire("client_B", tokens_requested=150, now=now)
    assert res.allowed is False
    assert res.reason == "TPM Exceeded"
    # Crucial Invariant: All-or-Nothing Atomic Guarantee
    # Since TPM failed, RPM tokens must NOT be deducted!
    assert res.remaining_rpm == 10.0
    assert res.remaining_tpm == 100.0
    # Over-capacity request permanently exceeds bucket capacity
    assert res.retry_after_seconds == float("inf")


def test_refill_over_time():
    limiter = DualTokenBucketLimiter(max_rpm=60.0, max_tpm=6000.0)
    now = 1000.0

    # Consume all RPM (60 reqs with 1 token each)
    for _ in range(60):
        limiter.acquire("client_C", tokens_requested=1, now=now)

    res_blocked = limiter.acquire("client_C", tokens_requested=1, now=now)
    assert res_blocked.allowed is False

    # Advance time by 30 seconds (half of 1 minute)
    # Refill rate: 60 / 60 = 1 req/sec -> 30 requests restored
    now_later = now + 30.0
    res_refilled = limiter.acquire("client_C", tokens_requested=1, now=now_later)
    assert res_refilled.allowed is True
    assert res_refilled.remaining_rpm >= 28.0


def test_refill_boundaries_and_cap():
    """Verify that tokens cannot accumulate beyond the configured max capacity."""
    limiter = DualTokenBucketLimiter(max_rpm=60.0, max_tpm=1000.0)
    now = 1000.0

    # Consume 100 tokens
    limiter.acquire("client_cap", tokens_requested=100, now=now)

    # Fast forward by 10 hours
    now_way_later = now + 36000.0
    res = limiter.acquire("client_cap", tokens_requested=10, now=now_way_later)
    assert res.allowed is True
    # Tokens refilled to max capacity minus cost
    assert res.remaining_rpm == pytest.approx(59.0)
    assert res.remaining_tpm == pytest.approx(990.0)


def test_clock_skew_tolerance():
    """Verify that client clock drifting backwards does not cause errors or negative refill."""
    limiter = DualTokenBucketLimiter(max_rpm=60.0, max_tpm=1000.0)
    now = 2000.0

    res1 = limiter.acquire("client_skew", tokens_requested=100, now=now)
    assert res1.allowed is True

    # Clock skews backwards by 50 seconds
    res2 = limiter.acquire("client_skew", tokens_requested=100, now=now - 50.0)
    assert res2.allowed is True
    # Decremented safely from previous state without negative elapsed glitch
    assert res2.remaining_rpm == pytest.approx(58.0)
    assert res2.remaining_tpm == pytest.approx(800.0)


def test_invalid_parameters():
    with pytest.raises(ValueError):
        DualTokenBucketLimiter(max_rpm=-1.0)
    with pytest.raises(ValueError):
        DualTokenBucketLimiter(max_tpm=0.0)

    limiter = DualTokenBucketLimiter()
    with pytest.raises(ValueError):
        limiter.acquire("client_X", tokens_requested=0)
    with pytest.raises(ValueError):
        limiter.acquire("client_X", tokens_requested=-10)
