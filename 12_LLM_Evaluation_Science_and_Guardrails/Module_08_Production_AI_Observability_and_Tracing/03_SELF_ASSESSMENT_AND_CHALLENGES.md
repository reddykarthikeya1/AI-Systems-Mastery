# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is standard APM tracing (e.g. Datadog HTTP tracing) insufficient for LLMs?
   - *Answer*: Traditional APM measures request duration but is blind to streaming token counts, TTFT vs TPOT, prompt/completion payloads, and model monetary costs.
2. What is the danger of logging full prompt and completion text in observability traces?
   - *Answer*: Data privacy and compliance violations: prompts frequently contain user PII, passwords, or confidential enterprise documents that should not reside in unencrypted log aggregators.
3. How does high TTFT indicate GPU cluster bottleneck?
   - *Answer*: High TTFT indicates prefill queue saturation or long KV cache allocation delays in continuous batching serving engines.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: High-Throughput OTel Exporter for 50M Daily LLM Tokens
**Context**: An enterprise SaaS application processes 50 million tokens per day. Synchronously emitting traces to Langfuse / Arize Phoenix causes client latency spikes.
**Question**: Architect the production observability pipeline.
**Solution**:
1. Buffer OTel spans in an in-memory lock-free ring buffer inside each application worker.
2. Background daemon thread flushes batches of 500 spans every 2 seconds via gRPC to an OpenTelemetry Collector.
3. Deploy sampling policies: record 100% of errors and guardrail blocks, but sample only 5% of successful turns.
