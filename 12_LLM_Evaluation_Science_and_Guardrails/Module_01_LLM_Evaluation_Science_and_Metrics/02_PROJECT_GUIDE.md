# Project Guide: Building a Production RAG Triad Evaluation Engine

In this project, you will build an automated evaluation engine that computes deterministic token metrics (Exact Match, Token F1) and RAG Triad metrics (Faithfulness, Answer Relevance, Context Precision).

---

## Three-Tier Implementation Path

### Tier 1: Deterministic Lexical & Token Metrics (Required)
- Implement `exact_match(prediction, target) -> float`.
- Implement `token_f1(prediction, target) -> float` with case folding and punctuation stripping.

### Tier 2: Atomic Claim Decomposition & Faithfulness Scoring
- Implement propositional claim splitting: breaks complex responses into atomic facts.
- Evaluate entailment of each claim against reference context using semantic overlap.

### Tier 3: Production RAG Triad Scoring Pipeline
- Combine Faithfulness, Answer Relevance, and Context Precision into a single unified `EvaluationReport`.
- Flag responses that fail the 85% groundedness threshold.
