"""Problem 01 — Otel Span Duration Aggregator

Topic: 08 Production AI Observability and Tracing
Target: Production-grade implementation

Compute total span duration and error count from OpenTelemetry trace spans.

Example:
    >>> spans = [{'name': 'llm_call', 'duration_ms': 250.5, 'has_error': False}, {'name': 'db_query', 'duration_ms': 45.2, 'has_error': True}]
    >>> otel_span_duration_aggregator(spans)
    {'total_duration_ms': 295.7, 'max_span_ms': 250.5, 'error_count': 1}

Hints:
    Hint 1: This is three independent aggregations over the same list — a
        running sum, a running max, and a running count — computed
        without depending on each other.
    Hint 2: Use sum() over each span's 'duration_ms' for the total, max()
        over the same field for the peak, and a count of spans where
        'has_error' is True, then round the two duration figures to 2
        decimals.
    Hint 3: An empty spans list can't call max() on an empty sequence, so
        it needs its own branch returning zeros for every field instead
        of letting max() raise a ValueError.
"""

from __future__ import annotations


def otel_span_duration_aggregator(spans: list[dict]) -> dict[str, float | int]:
    """Each span dict has: {'name': str, 'duration_ms': float, 'has_error': bool}.
    Compute total_duration_ms, max_span_ms, and error_count.
    Returns dict with 'total_duration_ms', 'max_span_ms', 'error_count'.
    """
    raise NotImplementedError("Implement otel_span_duration_aggregator")
