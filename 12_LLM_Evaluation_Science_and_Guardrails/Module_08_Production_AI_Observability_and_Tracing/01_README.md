# Module 08: Production AI Observability and Tracing

---

## 🗺️ Recommended Step-by-Step Learning Path

Follow this exact sequence to achieve complete mastery of this module:

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[01_README.md](01_README.md)** | Read conceptual overview, architectural foundations, and mental models. |
| **2** | **[00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md)** | Practice beginner spoonfed micro-drills and line-by-line syntax breakdowns. |
| **3** | **[00_try_it_yourself.py](00_try_it_yourself.py)** | Run in terminal (`python 00_try_it_yourself.py`) for an interactive zero-dependency sandbox. |
| **4** | **[04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md)** | Study forensic runbooks, edge cases, and real-world failure post-mortems. |
| **5** | **[03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test your knowledge with self-assessment quizzes, challenges, and diagnostic scenarios. |
| **6** | **[02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md)** | Follow guided project implementation for `starter/` and `project_solution/`. |
| **7** | **[problems/](problems/)** | Solve hands-on problem bank challenges and verify with `pytest problems/tests`. |
| **8** | **[debug_lab/](debug_lab/)** | Diagnose and fix silent production bugs in the Bug Hunter Drill. |

---

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
