"""Beginner playground for Module 08 - Production AI Observability & Tracing.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import time
import json

# -------------------------------------------- 1. OpenTelemetry Span Hierarchy
trace = {
    "trace_id": "tr_987654321",
    "root_span": "agent_execution",
    "children": [
        {"span_id": "sp_1", "name": "retrieval", "duration_ms": 42.0},
        {"span_id": "sp_2", "name": "llm_generate", "duration_ms": 280.0}
    ]
}

total_duration = sum(c["duration_ms"] for c in trace["children"])
assert len(trace["children"]) == 2
assert total_duration == 322.0
print(f"Distributed trace captured {len(trace['children'])} spans totaling {total_duration} ms.")

# -------------------------------------------- 2. Token Usage and Cost Accounting
prompt_tokens = 1500
completion_tokens = 300
price_input_per_million = 3.00   # $3.00 per 1M input tokens
price_output_per_million = 15.00 # $15.00 per 1M output tokens

cost = (prompt_tokens * price_input_per_million / 1e6) + (completion_tokens * price_output_per_million / 1e6)

assert abs(cost - (0.0045 + 0.0045)) < 1e-6
assert cost == 0.009
print(f"Request token cost: ${cost:.5f} ({prompt_tokens} prompt, {completion_tokens} completion)")

# -------------------------------------------- 3. Error Rate and Latency SLO Monitoring
success_requests = 999
error_requests = 1
total_reqs = success_requests + error_requests
error_rate = error_requests / total_reqs

assert error_rate == 0.001
assert error_rate <= 0.001, "Meets 99.9% availability SLO"
print(f"System error rate: {error_rate:.3%} (SLO satisfied)")

print()
print("All checks passed.")
