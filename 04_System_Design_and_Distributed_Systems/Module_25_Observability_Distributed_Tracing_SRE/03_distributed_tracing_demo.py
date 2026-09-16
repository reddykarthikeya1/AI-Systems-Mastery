"""Module 25: Standalone Interactive Demo - Distributed Tracing & SRE Resilience."""

import time

from project_solution.resilience_telemetry import (
    CircuitBreaker,
    CircuitBreakerOpenException,
    DistributedTracer,
    ResilienceMath,
    W3CTraceContext,
)


def main() -> None:
    print("=" * 80)
    print(" MODULE 25: OBSERVABILITY, DISTRIBUTED TRACING & SRE RESILIENCE")
    print("=" * 80)

    # ---------------------------------------------------------
    # Part 1: Distributed Tracing & W3C Traceparent Propagation
    # ---------------------------------------------------------
    print("\n--- 1. W3C Distributed Trace Context Propagation ---")
    tracer = DistributedTracer()

    # Hop 1: API Gateway receives incoming external request
    root_span = tracer.start_span("api_gateway_ingress", attributes={"http.path": "/checkout"})
    time.sleep(0.01)
    traceparent_hop1 = W3CTraceContext.format_header(root_span.trace_id, root_span.span_id)
    print(f" [API Gateway] Generated W3C Header: {traceparent_hop1}")

    # Hop 2: Auth Service verifies credentials
    auth_span = tracer.start_span("auth_service_validate", parent_traceparent=traceparent_hop1)
    time.sleep(0.005)
    auth_span.add_event("jwt_verified", {"user_id": "usr_42"})
    tracer.end_span(auth_span)

    # Hop 3: Payment Service charges card
    pay_span = tracer.start_span("payment_service_charge", parent_traceparent=traceparent_hop1)
    time.sleep(0.015)
    pay_span.add_event("stripe_charge_created", {"charge_id": "ch_789"})
    tracer.end_span(pay_span)

    tracer.end_span(root_span)

    # Render Trace Hierarchy Tree
    trace_spans = tracer.get_trace_spans(root_span.trace_id)
    print(f"\n Trace Visualization (Trace ID: {root_span.trace_id}):")
    for s in trace_spans:
        indent = "  " if s.parent_span_id else ""
        parent_str = f"parent={s.parent_span_id[:8]}" if s.parent_span_id else "ROOT"
        print(f" {indent}|-- [{s.name:<24}] SpanId: {s.span_id[:8]} ({parent_str}) | Latency: {s.duration_ms:.2f}ms")

    # ---------------------------------------------------------
    # Part 2: 3-State Circuit Breaker Fault Isolation
    # ---------------------------------------------------------
    print("\n--- 2. 3-State Circuit Breaker (Closed -> Open -> Half-Open -> Closed) ---")
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout_sec=2.0, half_open_success_threshold=2)
    print(f" Initial State: {cb.state.value} (Failure Threshold: {cb.failure_threshold})")

    def flaky_payment_gateway(fail: bool) -> str:
        if fail:
            raise ConnectionError("504 Gateway Timeout connecting to payment rail")
        return "200 OK: Payment Processed"

    # Simulate 3 failures
    current_sim_time = 100.0
    for i in range(1, 4):
        try:
            cb.call(flaky_payment_gateway, fail=True, current_time=current_sim_time)
        except ConnectionError:
            print(f" Attempt {i}: Call failed -> Failures={cb.consecutive_failures}/{cb.failure_threshold} | State={cb.state.value}")

    print(f"\n >>> Circuit Breaker Tripped to {cb.state.value}! Subsequent requests fail fast:")

    # Attempt call while OPEN (should fail fast without invoking function)
    try:
        cb.call(flaky_payment_gateway, fail=False, current_time=current_sim_time + 0.5)
    except CircuitBreakerOpenException as e:
        print(f" Fast Fail Result: '{e}' (0ms latency, protected downstream!)")

    # Fast forward time past recovery timeout (2.0s) -> Enters HALF-OPEN
    current_sim_time += 2.5
    print("\n >>> Simulated time advanced past recovery timeout. Next calls enter HALF-OPEN probe:")

    probe1 = cb.call(flaky_payment_gateway, fail=False, current_time=current_sim_time)
    print(f" Probe 1: Success={probe1} | State={cb.state.value} | Probes={cb.consecutive_successes}/{cb.half_open_success_threshold}")

    probe2 = cb.call(flaky_payment_gateway, fail=False, current_time=current_sim_time + 0.1)
    print(f" Probe 2: Success={probe2} | State={cb.state.value} (Fully Healed and Restored!)")

    # ---------------------------------------------------------
    # Part 3: SRE SLI / SLO Error Budget & Full Jitter Math
    # ---------------------------------------------------------
    print("\n--- 3. Site Reliability Engineering (SRE) SLO Math & Full Jitter ---")
    slo_metrics = ResilienceMath.calculate_slo_metrics(total_requests=10000, successful_requests=9985, slo_target=0.999)
    print(f" Measured SLI:              {slo_metrics['sli'] * 100:.3f}% (Target: {slo_metrics['slo_target'] * 100}%)")
    print(f" Error Budget Remaining:    {slo_metrics['error_budget_remaining'] * 100:.1f}%")
    print(f" Budget Burn Factor:        {slo_metrics['burn_rate']:.2f}x")

    backoffs = [ResilienceMath.full_jitter_backoff(attempt=i, base_sec=0.1, cap_sec=2.0) for i in range(4)]
    print(f" Sample Full Jitter Backoff Schedule: {[round(b, 3) for b in backoffs]} seconds")

    print("=" * 80)


if __name__ == "__main__":
    main()
