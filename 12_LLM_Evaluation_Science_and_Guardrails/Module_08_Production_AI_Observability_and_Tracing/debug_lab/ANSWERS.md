# Debug Lab Solution & Forensic Post-Mortem

## Incident: Observability Tracer Drops Latency, Time-to-First-Token, and Cost From Every LLM Call Trace

---

### 🔍 Forensic Root Cause Analysis
`record()` only accepts a model name and a token count, and its return value is a bare dictionary built from just that:

```python
def record(self, model, tokens):
    return {"tokens": tokens}
```

There is no parameter for call duration/latency, no parameter for time-to-first-token, and no per-token or per-call cost computation of any kind. Because the function signature itself never receives that data, no caller can pass it in, and no downstream trace record can ever contain it -- this is not a bug in some calculation that silently produces a wrong latency or cost value; the fields simply do not exist anywhere in the schema `record()` builds. A cost dashboard or SLA alert reading these traces has no data to work with, not incorrect data.

---

### 🛠️ Production Corrective Action & Code Fix

```python
PRICE_PER_1K_TOKENS = {"gpt-4o": 0.005}

class FixedTracer:
    def record(self, model, tokens, latency_ms, ttft_ms):
        cost = (tokens / 1000) * PRICE_PER_1K_TOKENS.get(model, 0.0)
        return {
            "model": model,
            "tokens": tokens,
            "latency_ms": latency_ms,
            "ttft_ms": ttft_ms,
            "cost_usd": round(cost, 6),
        }
```

Accepting `latency_ms` and `ttft_ms` as parameters and computing `cost_usd` from the token count and a price table means the emitted trace now carries every field a cost or latency dashboard actually needs, sourced from the real call instead of omitted entirely.

---

### 🛡️ Production Prevention Invariants
1. **Trace Schemas Must Include Latency, TTFT, and Cost From Day One:** Retrofitting these fields only after an incident means the incident itself leaves no data behind to investigate.
2. **Add a Schema/Contract Test on Emitted Trace Records:** Assert every trace contains the full set of fields the cost dashboard and SLA alerting depend on, so a missing field is caught in CI, not in production.
3. **Alert on Missing or Zero-Valued Cost/Latency Fields:** Treat their absence as a data-quality signal in its own right, not just an input to the aggregated dashboard numbers.
