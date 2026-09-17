"""Unit and integration test suite for Module 25: Observability & SRE Resilience."""

import pytest
from resilience_telemetry import (
    CircuitBreaker,
    CircuitBreakerOpenException,
    CircuitBreakerState,
    DistributedTracer,
    ResilienceMath,
    W3CTraceContext,
)


def test_w3c_traceparent_header_generation_and_parsing() -> None:
    trace_id = "4bf92f3577b34da6a3ce929d0e0e4736"
    span_id = "00f067aa0ba902b7"
    header = W3CTraceContext.format_header(trace_id, span_id, sampled=True)
    assert header == f"00-{trace_id}-{span_id}-01"

    parsed_trace, parsed_span, sampled = W3CTraceContext.parse_header(header)
    assert parsed_trace == trace_id
    assert parsed_span == span_id
    assert sampled is True

    # Invalid header
    with pytest.raises(ValueError):
        W3CTraceContext.parse_header("invalid-header-string")


def test_distributed_tracer_parent_child_linking() -> None:
    tracer = DistributedTracer()

    root = tracer.start_span("root_op")
    root_header = W3CTraceContext.format_header(root.trace_id, root.span_id)

    child = tracer.start_span("child_op", parent_traceparent=root_header)
    tracer.end_span(child)
    tracer.end_span(root)

    assert child.trace_id == root.trace_id
    assert child.parent_span_id == root.span_id
    assert root.parent_span_id is None

    spans = tracer.get_trace_spans(root.trace_id)
    assert len(spans) == 2


def test_circuit_breaker_state_transitions() -> None:
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout_sec=10.0, half_open_success_threshold=2)

    def failing_fn():
        raise RuntimeError("DB Down")

    def ok_fn():
        return "SUCCESS"

    t = 100.0
    # Failure 1: Still CLOSED
    with pytest.raises(RuntimeError):
        cb.call(failing_fn, current_time=t)
    assert cb.state == CircuitBreakerState.CLOSED

    # Failure 2: Hits threshold -> Transitions to OPEN
    with pytest.raises(RuntimeError):
        cb.call(failing_fn, current_time=t)
    assert cb.state == CircuitBreakerState.OPEN

    # Call at t=105s (before 10s timeout): Fast fails with CircuitBreakerOpenException
    with pytest.raises(CircuitBreakerOpenException):
        cb.call(ok_fn, current_time=t + 5.0)

    # Call at t=111s: Timeout elapsed -> Enters HALF_OPEN and executes ok_fn
    res1 = cb.call(ok_fn, current_time=t + 11.0)
    assert res1 == "SUCCESS"
    assert cb.state == CircuitBreakerState.HALF_OPEN

    # Second successful probe heals to CLOSED
    res2 = cb.call(ok_fn, current_time=t + 12.0)
    assert res2 == "SUCCESS"
    assert cb.state == CircuitBreakerState.CLOSED


def test_circuit_breaker_half_open_failure_re_trip() -> None:
    cb = CircuitBreaker(failure_threshold=1, recovery_timeout_sec=5.0)

    def failing_fn():
        raise RuntimeError("Crash")

    # Trip to OPEN
    with pytest.raises(RuntimeError):
        cb.call(failing_fn, current_time=0.0)
    assert cb.state == CircuitBreakerState.OPEN

    # Enter HALF_OPEN at t=6.0s but fail again
    with pytest.raises(RuntimeError):
        cb.call(failing_fn, current_time=6.0)
    # Must immediately re-trip back to OPEN
    assert cb.state == CircuitBreakerState.OPEN


def test_resilience_full_jitter_bounds() -> None:
    for attempt in range(5):
        sleep_time = ResilienceMath.full_jitter_backoff(attempt=attempt, base_sec=0.1, cap_sec=1.0)
        max_possible = min(1.0, 0.1 * (2 ** attempt))
        assert 0.0 <= sleep_time <= max_possible


def test_sre_slo_metrics_calculation() -> None:
    # 10,000 requests, 9,990 success -> 99.9% SLI (Target 99.9%) -> 0 error budget remaining
    metrics = ResilienceMath.calculate_slo_metrics(total_requests=10000, successful_requests=9990, slo_target=0.999)
    assert metrics["sli"] == pytest.approx(0.999)
    assert metrics["error_budget_remaining"] == pytest.approx(0.0)

    # 10,000 requests, 9,995 success -> 99.95% SLI -> 50% budget remaining
    metrics2 = ResilienceMath.calculate_slo_metrics(total_requests=10000, successful_requests=9995, slo_target=0.999)
    assert metrics2["sli"] == pytest.approx(0.9995)
    assert metrics2["error_budget_remaining"] == pytest.approx(0.5)
