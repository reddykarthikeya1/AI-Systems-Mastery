# Recommended Reading - LLM Evaluation Science and Guardrails

Written explainers (official docs, university notes, standard references, well-known engineering blogs) for every module concept.
Each page was fetched and its text read by a script that checks the page actually names the concepts listed under `Covers`.
Use these when a video is not enough or you prefer text; then do the module exercises.

### Module 01: LLM Evaluation Science: Ground Truth & RAGAS

- [Ragas](https://docs.ragas.io/en/stable/) | **docs.ragas.io** | Covers: RAGAS
- [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/) | **eugeneyan.com** | Covers: LLM Evaluation Science
- [Ground truth - Wikipedia](https://en.wikipedia.org/wiki/Ground_truth) | **en.wikipedia.org** | Covers: Ground Truth
- [Metrics - Ragas](https://docs.ragas.io/en/stable/concepts/metrics/) | **docs.ragas.io** | Covers: RAGAS

### Module 02: LLM-as-a-Judge Calibration & Bias Mitigation

- [Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)](https://eugeneyan.com/writing/llm-evaluators/) | **eugeneyan.com** | Covers: LLM-as-a-Judge Calibration, Bias Mitigation
- [Using LLM-as-a-Judge For Evaluation: A Complete Guide – Hamel’s Blog](https://hamel.dev/blog/posts/llm-judge/) | **hamel.dev** | Covers: LLM-as-a-Judge Calibration, Bias Mitigation
- [[2306.05685] Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) | **arxiv.org** | Covers: LLM-as-a-Judge Calibration
- [Using LLM-as-a-judge 🧑‍⚖️ for an automated and versatile evaluation · Hugging Face](https://huggingface.co/learn/cookbook/llm_judge) | **huggingface.co** | Covers: LLM-as-a-Judge Calibration

### Module 03: Benchmark Harnesses (MMLU, GSM8K, HumanEval)

- [GitHub - EleutherAI/lm-evaluation-harness: A framework for few-shot evaluation of language models. ·](https://github.com/EleutherAI/lm-evaluation-harness) | **github.com** | Covers: Benchmark Harnesses, MMLU, GSM8K
- [GitHub - openai/human-eval: Code for the paper "Evaluating Large Language Models Trained on Code" · ](https://github.com/openai/human-eval) | **github.com** | Covers: Benchmark Harnesses, HumanEval
- [[2110.14168] Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168) | **arxiv.org** | Covers: GSM8K

### Module 04: Production Guardrails Architecture & Policy Filters

- [Overview | NVIDIA NeMo Guardrails Library Developer Guide](https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/overview) | **docs.nvidia.com** | Covers: Production Guardrails Architecture, Policy Filters
- [Generative AI Data Governance – Amazon Bedrock Guardrails – AWS](https://aws.amazon.com/bedrock/guardrails/) | **aws.amazon.com** | Covers: Production Guardrails Architecture, Policy Filters
- [Introduction - Guardrails AI](https://guardrailsai.com/guardrails/docs) | **guardrailsai.com** | Covers: Production Guardrails Architecture
- [Moderation | OpenAI API](https://developers.openai.com/api/docs/guides/moderation) | **platform.openai.com** | Covers: Policy Filters
- [What is Azure AI Content Safety? - Azure AI services | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview) | **learn.microsoft.com** | Covers: Policy Filters

### Module 05: NVIDIA NeMo Guardrails & Meta Llama Guard

- [Overview | NVIDIA NeMo Guardrails Library Developer Guide](https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/overview) | **docs.nvidia.com** | Covers: NVIDIA NeMo Guardrails, Meta Llama Guard
- [meta-llama/Llama-Guard-3-8B · Hugging Face](https://huggingface.co/meta-llama/Llama-Guard-3-8B) | **huggingface.co** | Covers: Meta Llama Guard
- [GitHub - NVIDIA-NeMo/Guardrails: NeMo Guardrails is an open-source toolkit for easily adding program](https://github.com/NVIDIA-NeMo/Guardrails) | **github.com** | Covers: NVIDIA NeMo Guardrails

### Module 06: Adversarial AI Security & OWASP Top 10 for LLMs

- [AI 100-2 E2025, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations ](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) | **csrc.nist.gov** | Covers: Adversarial AI Security, OWASP Top 10 for LLMs
- [OWASP Foundation](https://owasp.org/projects/top-10-for-large-language-model-applications) | **owasp.org** | Covers: OWASP Top 10 for LLMs
- [LLMRisks Archive - OWASP Gen AI Security Project](https://genai.owasp.org/llm-top-10/) | **genai.owasp.org** | Covers: OWASP Top 10 for LLMs
- [Simon Willison: Prompt injection](https://simonwillison.net/series/prompt-injection/) | **simonwillison.net** | Covers: OWASP Top 10 for LLMs
- [AI Risk Management Framework | NIST](https://www.nist.gov/itl/ai-risk-management-framework) | **nist.gov** | Covers: OWASP Top 10 for LLMs

### Module 07: Automated Red Teaming & Jailbreak Testing (PyRIT)

- [LLM red teaming guide (open source) | Promptfoo](https://www.promptfoo.dev/docs/red-team/) | **promptfoo.dev** | Covers: Automated Red Teaming, Jailbreak Testing
- [PyRIT Documentation](https://microsoft.github.io/PyRIT/) | **azure.github.io** | Covers: PyRIT
- [GitHub - Azure/PyRIT: The Python Risk Identification Tool for generative AI (PyRIT) is an open sourc](https://github.com/Azure/PyRIT) | **github.com** | Covers: PyRIT
- [GitHub - NVIDIA/garak: the LLM vulnerability scanner · GitHub](https://github.com/NVIDIA/garak) | **github.com** | Covers: Automated Red Teaming

### Module 08: Production AI Observability & OpenTelemetry Tracing

- [Traces | OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/traces/) | **opentelemetry.io** | Covers: Production AI Observability, OpenTelemetry Tracing
- [Moved: Generative AI semantic conventions | OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | **opentelemetry.io** | Covers: OpenTelemetry Tracing
- [LLM Observability & Application Tracing (Open Source) - Langfuse](https://langfuse.com/docs/observability/overview) | **langfuse.com** | Covers: Production AI Observability
- [LangSmith Observability - Docs by LangChain](https://docs.langchain.com/langsmith/observability) | **docs.smith.langchain.com** | Covers: Production AI Observability
