"""Reference Solution — Problem 01: Otel Span Duration Aggregator

Topic: 08 Production AI Observability and Tracing
"""

from __future__ import annotations


def otel_span_duration_aggregator(spans: list[dict]) -> dict[str, float | int]:
    if not spans:
        return {'total_duration_ms': 0.0, 'max_span_ms': 0.0, 'error_count': 0}
    total = sum(s.get('duration_ms', 0.0) for s in spans)
    m = max(s.get('duration_ms', 0.0) for s in spans)
    errs = sum(1 for s in spans if s.get('has_error', False))
    return {
        'total_duration_ms': round(total, 2),
        'max_span_ms': round(m, 2),
        'error_count': errs
    }
