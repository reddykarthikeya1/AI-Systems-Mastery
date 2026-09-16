# Module 08: Production AI Observability and Tracing

## 1. OpenTelemetry Semantic Conventions for Generative AI

The OpenTelemetry (OTel) GenAI working group specifies standard attribute keys for LLM monitoring:

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `gen_ai.system` | string | Vendor / provider identifier (`openai`, `anthropic`, `vllm`) |
| `gen_ai.request.model` | string | Target model identifier (`gpt-4o`, `claude-3-5-sonnet`) |
| `gen_ai.usage.prompt_tokens` | int | Number of prompt tokens ingested |
| `gen_ai.usage.completion_tokens` | int | Number of generated tokens emitted |
| `gen_ai.response.finish_reasons` | string[] | Array of termination reasons (`stop`, `length`, `tool_calls`) |

---

## 2. Latency Metrics: TTFT and TPOT

$$\text{Total Latency} = \text{TTFT} + (N_{\text{completion}} - 1) \times \text{TPOT}$$

- **Time-to-First-Token (TTFT)**: Measures prompt prefill latency and queuing time.
- **Time-per-Output-Token (TPOT)**: Measures autoregressive decoding throughput.

---

## 3. Real-Time Cost Calculation

$$\text{Cost} = (N_{\text{prompt}} \times P_{\text{prompt}}) + (N_{\text{completion}} \times P_{\text{completion}})$$

Production tracing systems aggregate cost per user, per API key, and per application feature in real time, firing alerts when rate limits or budget thresholds are approached.
