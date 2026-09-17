# 🐣 Interactive Foundations Playground: Production AI Observability & Tracing

> *"Observability tracks every token from user prompt to final response with OpenTelemetry spans."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import time
import json
```

---

## 1. OpenTelemetry Span Hierarchy

A root trace encapsulates parent spans (Agent Loop) and child spans (LLM Generation, Vector Retrieval, Tool Execution).

```python
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
```

---

## 2. Token Usage and Cost Accounting

Tracking input and output token consumption and calculating real-time API dollar costs.

```python
prompt_tokens = 1500
completion_tokens = 300
price_input_per_million = 3.00   # $3.00 per 1M input tokens
price_output_per_million = 15.00 # $15.00 per 1M output tokens

cost = (prompt_tokens * price_input_per_million / 1e6) + (completion_tokens * price_output_per_million / 1e6)

assert abs(cost - (0.0045 + 0.0045)) < 1e-6
assert cost == 0.009
print(f"Request token cost: ${cost:.5f} ({prompt_tokens} prompt, {completion_tokens} completion)")
```

---

## 3. Error Rate and Latency SLO Monitoring

Monitoring P99 latency and 5xx error rate to maintain 99.9% uptime Service Level Objectives.

```python
success_requests = 999
error_requests = 1
total_reqs = success_requests + error_requests
error_rate = error_requests / total_reqs

assert error_rate == 0.001
assert error_rate <= 0.001, "Meets 99.9% availability SLO"
print(f"System error rate: {error_rate:.3%} (SLO satisfied)")
```

---
