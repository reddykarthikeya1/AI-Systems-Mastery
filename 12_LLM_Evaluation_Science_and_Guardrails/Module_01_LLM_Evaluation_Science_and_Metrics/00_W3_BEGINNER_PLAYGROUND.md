# Beginner Playground: LLM Evaluation Science & RAG Triad

Welcome to LLM Evaluation! In traditional software engineering, a function either returns `True` or `False`. With LLMs, outputs are probabilistic, open-ended, and subtly nuanced.

---

## 1. The Core Mental Model: The RAG Triad

When evaluating a Retrieval-Augmented Generation (RAG) system, three core questions determine end-to-end quality:

```
                  [ User Query ]
                  /            \
  (Context Relevance)       (Answer Relevance)
                /                \
               v                  v
     [ Retrieved Context ] ---> [ Generated Answer ]
                \                /
                 (Faithfulness / Groundedness)
```

1. **Context Relevance (Precision)**: Is the retrieved context focused on the user query without irrelevant noise?
2. **Faithfulness (Groundedness)**: Can every claim in the generated answer be directly inferred from the retrieved context (Zero Hallucination)?
3. **Answer Relevance**: Does the generated answer directly answer what the user asked?

---

## 2. Interactive Pure-Python Experiment: Token F1 & Faithfulness Verifier

```python
import re
from typing import Set

def tokenize(text: str) -> Set[str]:
    return set(re.findall(r"\w+", text.lower()))

def token_f1_score(prediction: str, ground_truth: str) -> float:
    pred_tokens = tokenize(prediction)
    truth_tokens = tokenize(ground_truth)

    if not pred_tokens or not truth_tokens:
        return 0.0

    common = pred_tokens.intersection(truth_tokens)
    if not common:
        return 0.0

    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(truth_tokens)
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1

def check_groundedness(claims: list[str], context: str) -> float:
    """Calculates percentage of claims supported by the context."""
    context_tokens = tokenize(context)
    supported = 0
    for claim in claims:
        claim_tokens = tokenize(claim)
        # If over 60% of unique claim keywords are in context, consider grounded
        overlap = claim_tokens.intersection(context_tokens)
        if len(overlap) / len(claim_tokens) >= 0.6:
            supported += 1
    return supported / len(claims) if claims else 1.0

ctx = "NVIDIA H100 SXM5 GPU features 80GB of HBM3 memory and 3.35 TB/s bandwidth."
claims = [
    "H100 has 80GB HBM3 memory",
    "Bandwidth is 3.35 TB/s",
    "It consumes 200 Watts" # Hallucinated claim
]

print(f"Token F1 Score: {token_f1_score('80GB HBM3 memory', ctx):.2f}")
print(f"Faithfulness Score: {check_groundedness(claims, ctx):.2f}")
```
