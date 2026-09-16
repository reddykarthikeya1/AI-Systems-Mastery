# Course 12: Master Syllabus & Learning Outcomes

## Detailed Module Breakdown

### Module 01: LLM Evaluation Science and Metrics
- **Theoretical Foundations**: Lexical metrics (BLEU, ROUGE-L), semantic similarity (BERTScore), RAG Triad formulation.
- **Systems Architecture**: Propositional claim decomposition, token intersection groundedness scoring, context precision@k.
- **Laboratory**: Implementing `RAGTriadEvaluator` and deterministic token metrics.

### Module 02: LLM as a Judge Calibration and Bias
- **Theoretical Foundations**: Pairwise vs single-answer scoring, Position Bias, Verbosity Bias, Self-Enhancement Bias, Cohen's Kappa agreement coefficient.
- **Systems Architecture**: Swap-pair evaluation tournaments, tie-breaking heuristics, length-normalization penalty.
- **Laboratory**: Implementing `LLMJudgeCalibrator`.

### Module 03: Standardized Benchmark Harnesses
- **Theoretical Foundations**: MMLU, GSM8K, HumanEval, ARC, TruthfulQA, Chen et al. unbiased Pass@k formulation.
- **Systems Architecture**: Chain-of-thought numeric answer extraction, $n$-gram contamination auditing, perplexity probing.
- **Laboratory**: Implementing `BenchmarkHarness` with math suite and contamination detector.

### Module 04: Production Guardrails Architecture
- **Theoretical Foundations**: Pre-flight, in-flight streaming, and post-flight guardrails, HIPAA/GDPR PII compliance.
- **Systems Architecture**: Regex entity scrubbing, token pseudonymization, topic restriction policies.
- **Laboratory**: Implementing `ProductionGuardrailPipeline`.

### Module 05: NeMo Guardrails and Llama Guard
- **Theoretical Foundations**: NVIDIA NeMo Colang dialogue flows, canonical user intent extraction, MLCommons safety hazard taxonomy (S1-S6).
- **Systems Architecture**: Finite state machine dialog routing, pre-flight safety classifier interception.
- **Laboratory**: Implementing `NeMoColangEngine` and `LlamaGuardClassifier`.

### Module 06: Adversarial AI Security & OWASP Top 10
- **Theoretical Foundations**: OWASP Top 10 for LLMs (LLM01-LLM10), jailbreak mechanics (DAN, Crescendo, roleplay hijacking).
- **Systems Architecture**: Base64/Hex obfuscation detection and decoding, prompt injection regex scanners, threat classification.
- **Laboratory**: Implementing `AdversarialSecurityScanner`.

### Module 07: Automated Red Teaming
- **Theoretical Foundations**: Automated Red Teaming (ART), PAIR, GCG, Attack Success Rate (ASR) formulation.
- **Systems Architecture**: Multi-strategy prompt mutation (hypothetical, roleplay, educational), target probing, safety refusal judge.
- **Laboratory**: Implementing `AutomatedRedTeamer`.

### Module 08: Production AI Observability and Tracing
- **Theoretical Foundations**: OpenTelemetry GenAI Semantic Conventions, TTFT and TPOT latency metrics, real-time cost attribution.
- **Systems Architecture**: Nested span hierarchy, token counters, pricing lookup tables, OTel JSON exporter.
- **Laboratory**: Implementing `GenAITracer`.
