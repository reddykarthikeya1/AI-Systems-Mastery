"""Unit tests for GenAI Telemetry Tracer."""

from __future__ import annotations

import time
import pytest
from genai_telemetry_tracer import GenAITracer


@pytest.fixture
def tracer() -> GenAITracer:
    return GenAITracer(trace_id="trace_xyz123")


def test_span_hierarchy_and_duration(tracer: GenAITracer):
    parent = tracer.start_span("root_query")
    time.sleep(0.01)
    child = tracer.start_span("vector_retrieval", parent=parent)
    time.sleep(0.01)
    tracer.end_span(child)
    tracer.end_span(parent)

    assert child.parent_span_id == parent.span_id
    assert len(parent.children) == 1
    assert parent.duration_ms > 0.0
    assert child.duration_ms > 0.0


def test_otel_token_and_cost_calculation(tracer: GenAITracer):
    span = tracer.start_span("llm_generation")
    tracer.end_span(
        span,
        model="gpt-4o",
        prompt_tokens=1_000,
        completion_tokens=500,
        ttft_sec=0.05,
    )

    # Cost calculation: 1000 * 2.5e-6 + 500 * 10e-6 = 0.0025 + 0.0050 = 0.0075 USD
    expected_cost = 0.0075
    assert pytest.approx(span.attributes["gen_ai.usage.cost_usd"], 1e-5) == expected_cost
    assert span.attributes["gen_ai.usage.total_tokens"] == 1500
    assert span.attributes["gen_ai.latency.ttft_ms"] == 50.0


def test_export_otel_payload(tracer: GenAITracer):
    s1 = tracer.start_span("s1")
    tracer.end_span(s1, model="llama-3-70b", prompt_tokens=100, completion_tokens=100)

    payload = tracer.export_otel_payload()
    assert payload["trace_id"] == "trace_xyz123"
    assert payload["span_count"] == 1
    assert len(payload["spans"]) == 1
    assert "gen_ai.usage.cost_usd" in payload["spans"][0]["attributes"]
