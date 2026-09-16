"""OpenTelemetry-Compliant Generative AI Tracing and Observability Engine."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


MODEL_PRICING = {
    "gpt-4o": {"prompt": 2.50 / 1_000_000, "completion": 10.00 / 1_000_000},
    "claude-3-5-sonnet": {"prompt": 3.00 / 1_000_000, "completion": 15.00 / 1_000_000},
    "llama-3-70b": {"prompt": 0.80 / 1_000_000, "completion": 0.80 / 1_000_000},
}


@dataclass
class GenAISpan:
    span_id: str
    name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    parent_span_id: Optional[str] = None
    children: List[GenAISpan] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000.0


class GenAITracer:
    """Production Tracer capturing OTel GenAI metrics and cost telemetry."""

    def __init__(self, trace_id: str) -> None:
        self.trace_id = trace_id
        self.spans: List[GenAISpan] = []
        self._span_counter = 0

    def start_span(self, name: str, parent: Optional[GenAISpan] = None) -> GenAISpan:
        """Creates and starts a new trace span."""
        self._span_counter += 1
        span_id = f"span_{self._span_counter}"
        span = GenAISpan(
            span_id=span_id,
            name=name,
            start_time=time.perf_counter(),
            parent_span_id=parent.span_id if parent else None,
        )
        if parent:
            parent.children.append(span)
        self.spans.append(span)
        return span

    def end_span(
        self,
        span: GenAISpan,
        model: Optional[str] = None,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        ttft_sec: Optional[float] = None,
    ) -> None:
        """Closes span and calculates standard GenAI attributes and cost."""
        span.end_time = time.perf_counter()

        if model:
            span.attributes["gen_ai.request.model"] = model
            span.attributes["gen_ai.usage.prompt_tokens"] = prompt_tokens
            span.attributes["gen_ai.usage.completion_tokens"] = completion_tokens
            span.attributes["gen_ai.usage.total_tokens"] = prompt_tokens + completion_tokens

            if ttft_sec is not None:
                span.attributes["gen_ai.latency.ttft_ms"] = ttft_sec * 1000.0
                gen_duration = (span.duration_ms / 1000.0) - ttft_sec
                if completion_tokens > 1 and gen_duration > 0:
                    span.attributes["gen_ai.latency.tpot_ms"] = (gen_duration / (completion_tokens - 1)) * 1000.0

            # Compute cost
            pricing = MODEL_PRICING.get(model, {"prompt": 0.0, "completion": 0.0})
            cost = (prompt_tokens * pricing["prompt"]) + (completion_tokens * pricing["completion"])
            span.attributes["gen_ai.usage.cost_usd"] = cost

    def get_total_trace_cost(self) -> float:
        """Computes aggregated dollar cost of all spans in this trace."""
        return sum(span.attributes.get("gen_ai.usage.cost_usd", 0.0) for span in self.spans)

    def export_otel_payload(self) -> Dict[str, Any]:
        """Exports trace to OTel-compliant JSON dictionary."""
        return {
            "trace_id": self.trace_id,
            "span_count": len(self.spans),
            "total_cost_usd": self.get_total_trace_cost(),
            "spans": [
                {
                    "span_id": s.span_id,
                    "name": s.name,
                    "parent_id": s.parent_span_id,
                    "duration_ms": s.duration_ms,
                    "attributes": s.attributes,
                }
                for s in self.spans
            ],
        }
