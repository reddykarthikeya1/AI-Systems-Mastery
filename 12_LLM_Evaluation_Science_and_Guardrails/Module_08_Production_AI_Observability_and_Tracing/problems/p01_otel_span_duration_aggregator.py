"""Problem 01 — Otel Span Duration Aggregator

Topic: 08 Production AI Observability and Tracing
Target: Production-grade implementation

Compute total span duration and error count from OpenTelemetry trace spans.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def otel_span_duration_aggregator(spans: list[dict]) -> dict[str, float | int]:
    """Each span dict has: {'name': str, 'duration_ms': float, 'has_error': bool}.
    Compute total_duration_ms, max_span_ms, and error_count.
    Returns dict with 'total_duration_ms', 'max_span_ms', 'error_count'.
    """
    raise NotImplementedError("Implement otel_span_duration_aggregator")
