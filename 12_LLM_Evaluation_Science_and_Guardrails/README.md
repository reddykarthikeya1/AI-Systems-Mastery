# Course 12: LLM Evaluation Science, Guardrails & Safety

Implement rigorous evaluation harnesses, red teaming suites, and safety guardrails. Build deterministic sanitizers, semantic moderation classifiers, jailbreak probes, and automated LLM judge pipelines.

---

## 1. Course Architecture & Mental Model

This course covers the rigorous engineering discipline required to evaluate, calibrate, guard, and trace LLM systems in mission-critical production environments:

```
                  +----------------------------------------------+
                  |               User Input Query               |
                  +----------------------------------------------+
                                         |
                                         v
   +---------------------------------------------------------------------------+
   | Multi-Tier Guardrails Gateway                                             |
   | - Pre-Flight PII Masking & Regex Redaction (Presidio Pattern Engine)       |
   | - Adversarial Attack & Obfuscation Scanner (OWASP Top 10 LLM Scanner)     |
   | - NeMo Colang Dialog State Machine & Meta Llama Guard Taxonomy (S1-S6)    |
   +---------------------------------------------------------------------------+
                                         |
                                         v
   +---------------------------------------------------------------------------+
   | LLM Inference Engine & OpenTelemetry Observability                        |
   | - TTFT (Time-To-First-Token) & TPOT (Time-Per-Output-Token) Tracking      |
   | - Token Accounting & Real-Time Dollar Cost Monitoring (OTel GenAI)       |
   +---------------------------------------------------------------------------+
                                         |
                                         v
   +---------------------------------------------------------------------------+
   | Evaluation Science & Alignment Certification                              |
   | - RAG Triad Evaluator (Faithfulness, Relevance, Context Precision)        |
   | - LLM-as-a-Judge Swap-Pair Calibration (Positional & Verbosity Debiasing) |
   | - Standardized Benchmarks (Pass@k, MMLU, GSM8K, HumanEval Decontamination)|
   | - Automated Red Teaming (ART / Mutation Engine & Attack Success Rate)     |
   +---------------------------------------------------------------------------+
```

---

## 2. Module Index

| Module | Title | Core Focus | Project Solution |
| :--- | :--- | :--- | :--- |
| **01** | [LLM Evaluation Science & Metrics](Module_01_LLM_Evaluation_Science_and_Metrics/01_README.md) | Exact Match, Token F1, RAG Triad, Faithfulness | `ragas_triad_evaluator.py` |
| **02** | [LLM as a Judge Calibration & Bias](Module_02_LLM_as_a_Judge_Calibration_and_Bias/01_README.md) | Swap-Pair Evaluation, Position/Verbosity Bias, Cohen's $\kappa$ | `llm_judge_calibrator.py` |
| **03** | [Standardized Benchmark Harnesses](Module_03_Standardized_Benchmark_Harnesses/01_README.md) | Pass@k Estimator, GSM8K Extraction, Decontamination | `benchmark_harness_sim.py` |
| **04** | [Production Guardrails Architecture](Module_04_Production_Guardrails_Architecture/01_README.md) | Pre/Post-Flight Rails, PII Redaction, Topic Blocking | `production_guardrails_pipeline.py` |
| **05** | [NeMo Guardrails & Llama Guard](Module_05_NeMo_Guardrails_and_Llama_Guard/01_README.md) | Colang State Machines, Intent Routing, S1-S6 Hazard Taxonomy | `nemo_colang_state_machine.py` |
| **06** | [Adversarial AI Security & OWASP Top 10](Module_06_Adversarial_AI_Security_OWASP_Top_10/01_README.md) | Prompt Injection, Base64 Obfuscation, System Leakage | `adversarial_detector.py` |
| **07** | [Automated Red Teaming](Module_07_Automated_Red_Teaming/01_README.md) | Adversarial Mutation Engine, Target Probing, ASR Scoring | `automated_red_teamer.py` |
| **08** | [Production AI Observability & Tracing](Module_08_Production_AI_Observability_and_Tracing/01_README.md) | OpenTelemetry GenAI Spans, TTFT/TPOT, Cost Estimation | `genai_telemetry_tracer.py` |

---

## 3. Verification & Grading Loop

Every module adheres strictly to the repository test contract:
```bash
# Run interactive quickstart demonstration across all modules
python 00_quickstart_interactive_demo.py

# Run full automated test suite
pytest 12_LLM_Evaluation_Science_and_Guardrails -v
ruff check 12_LLM_Evaluation_Science_and_Guardrails
```
