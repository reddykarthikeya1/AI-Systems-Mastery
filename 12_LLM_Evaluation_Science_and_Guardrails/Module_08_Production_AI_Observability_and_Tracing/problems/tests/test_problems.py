"""Tests for Otel Span Duration Aggregator."""
from __future__ import annotations

import pytest
from p01_otel_span_duration_aggregator import otel_span_duration_aggregator


def test_otel_span_duration_aggregator():
    spans = [
        {'name': 'llm_call', 'duration_ms': 250.5, 'has_error': False},
        {'name': 'db_query', 'duration_ms': 45.2, 'has_error': True}
    ]
    res = otel_span_duration_aggregator(spans)
    assert res['total_duration_ms'] == 295.7
    assert res['max_span_ms'] == 250.5
    assert res['error_count'] == 1
