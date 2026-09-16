"""Module 25: Observability, Distributed Tracing & SRE Resilience Telemetry.

Reference implementation of W3C Trace Context propagation, Span DAG collector,
3-state Circuit Breaker, Exponential Backoff with Full Jitter, and SLO error budget math.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import enum
import random
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

# ============================================================================
# 1. W3C Distributed Tracing & Span Collector
# ============================================================================

@dataclass
class Span:
    name: str
    trace_id: str
    span_id: str
    parent_span_id: str | None
    start_time: float
    end_time: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        if self.end_time is None:
            return 0.0
        return max(0.0, (self.end_time - self.start_time) * 1000.0)

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        self.events.append({
            "name": name,
            "timestamp": time.time(),
            "attributes": attributes or {},
        })


class W3CTraceContext:
    """Encodes and parses standard W3C 'traceparent' headers."""

    @staticmethod
    def generate_trace_id() -> str:
        return uuid.uuid4().hex  # 32 hex chars (16 bytes)

    @staticmethod
    def generate_span_id() -> str:
        return uuid.uuid4().hex[:16]  # 16 hex chars (8 bytes)

    @classmethod
    def format_header(cls, trace_id: str, span_id: str, sampled: bool = True) -> str:
        flags = "01" if sampled else "00"
        return f"00-{trace_id}-{span_id}-{flags}"

    @classmethod
    def parse_header(cls, header: str) -> tuple[str, str, bool]:
        """Parses '00-{trace_id}-{span_id}-{flags}' into components."""
        parts = header.strip().split("-")
        if len(parts) != 4 or parts[0] != "00":
            raise ValueError(f"Invalid W3C traceparent header: {header}")
        trace_id = parts[1]
        span_id = parts[2]
        sampled = parts[3] == "01"
        return trace_id, span_id, sampled


class DistributedTracer:
    """Manages spans and builds end-to-end distributed execution trees."""

    def __init__(self) -> None:
        self.spans: list[Span] = []

    def start_span(
        self,
        name: str,
        parent_traceparent: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> Span:
        """Starts a new span linked to a parent W3C trace context if present."""
        if parent_traceparent:
            trace_id, parent_span_id, _ = W3CTraceContext.parse_header(parent_traceparent)
        else:
            trace_id = W3CTraceContext.generate_trace_id()
            parent_span_id = None

        span_id = W3CTraceContext.generate_span_id()
        span = Span(
            name=name,
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            start_time=time.time(),
            attributes=attributes or {},
        )
        self.spans.append(span)
        return span

    def end_span(self, span: Span) -> None:
        if span.end_time is None:
            span.end_time = time.time()

    def get_trace_spans(self, trace_id: str) -> list[Span]:
        """Returns all spans belonging to a trace, ordered by start time."""
        matched = [s for s in self.spans if s.trace_id == trace_id]
        matched.sort(key=lambda s: s.start_time)
        return matched


# ============================================================================
# 2. 3-State Circuit Breaker
# ============================================================================

class CircuitBreakerState(enum.StrEnum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpenException(Exception):
    """Raised when request is rejected fast due to an open circuit breaker."""
    pass


class CircuitBreaker:
    """Implements Michael Nygard / Netflix Hystrix 3-state circuit breaker."""

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout_sec: float = 5.0,
        half_open_success_threshold: int = 2,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.half_open_success_threshold = half_open_success_threshold

        self.state = CircuitBreakerState.CLOSED
        self.consecutive_failures = 0
        self.consecutive_successes = 0
        self.last_failure_time: float = 0.0

    def call(
        self,
        func: Callable[..., Any],
        *args: Any,
        current_time: float | None = None,
        **kwargs: Any,
    ) -> Any:
        """Executes func protected by the circuit breaker state machine."""
        if current_time is None:
            current_time = time.time()

        # 1. State Evaluation: If OPEN, check if recovery timeout has elapsed
        if self.state == CircuitBreakerState.OPEN:
            if current_time - self.last_failure_time >= self.recovery_timeout_sec:
                # Transition to HALF_OPEN probe state
                self.state = CircuitBreakerState.HALF_OPEN
                self.consecutive_successes = 0
            else:
                # Fail fast immediately
                raise CircuitBreakerOpenException(
                    "Circuit breaker is OPEN. Fast failing request to protect downstream."
                )

        # 2. Attempt Execution
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure(current_time)
            raise e

    def _on_success(self) -> None:
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.consecutive_successes += 1
            if self.consecutive_successes >= self.half_open_success_threshold:
                # Fully healed! Reset to CLOSED
                self.state = CircuitBreakerState.CLOSED
                self.consecutive_failures = 0
                self.consecutive_successes = 0
        elif self.state == CircuitBreakerState.CLOSED:
            self.consecutive_failures = 0

    def _on_failure(self, current_time: float) -> None:
        self.last_failure_time = current_time
        if self.state == CircuitBreakerState.HALF_OPEN:
            # Single failure in probe state trips back to OPEN immediately
            self.state = CircuitBreakerState.OPEN
            self.consecutive_successes = 0
        elif self.state == CircuitBreakerState.CLOSED:
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN


# ============================================================================
# 3. Exponential Backoff with Full Jitter & SRE Math
# ============================================================================

class ResilienceMath:
    """Calculates backoff intervals and SRE Service Level Objective metrics."""

    @staticmethod
    def full_jitter_backoff(
        attempt: int,
        base_sec: float = 0.1,
        cap_sec: float = 2.0,
        rng: random.Random | None = None,
    ) -> float:
        """AWS Full Jitter: Uniform(0, min(cap, base * 2^attempt))."""
        if rng is None:
            rng = random.Random()
        calculated_backoff = min(cap_sec, base_sec * (2 ** attempt))
        return rng.uniform(0.0, calculated_backoff)

    @staticmethod
    def calculate_slo_metrics(
        total_requests: int,
        successful_requests: int,
        slo_target: float = 0.999,
    ) -> dict[str, float]:
        """Computes SLI, Error Budget, and Error Budget consumption."""
        if total_requests == 0:
            return {"sli": 1.0, "error_budget_remaining": 1.0, "burn_rate": 0.0}

        actual_sli = successful_requests / float(total_requests)
        allowed_error_fraction = 1.0 - slo_target
        actual_error_fraction = 1.0 - actual_sli

        error_budget_consumed = actual_error_fraction / allowed_error_fraction if allowed_error_fraction > 0 else 1.0
        remaining_budget = max(0.0, 1.0 - error_budget_consumed)

        return {
            "sli": actual_sli,
            "slo_target": slo_target,
            "error_budget_remaining": remaining_budget,
            "burn_rate": error_budget_consumed,
        }
