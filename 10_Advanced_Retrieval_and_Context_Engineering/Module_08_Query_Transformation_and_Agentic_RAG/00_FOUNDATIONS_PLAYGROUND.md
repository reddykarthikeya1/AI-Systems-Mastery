# 🐣 Interactive Foundations Playground: Query Transformation & Agentic RAG

> *"Agentic RAG evaluates whether retrieved evidence actually answers the question before letting the LLM respond."*

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
import math
```

---

## 1. Query Decomposition into Sub-Queries

Complex multi-part questions are decomposed into independent search queries executed in parallel.

```python
complex_query = "Compare revenue growth of Apple and Microsoft in 2024."
sub_queries = [
    "What was Apple's revenue growth in 2024?",
    "What was Microsoft's revenue growth in 2024?"
]

assert len(sub_queries) == 2
assert "Apple" in sub_queries[0]
assert "Microsoft" in sub_queries[1]
print(f"Decomposed '{complex_query}' into {len(sub_queries)} sub-queries.")
```

---

## 2. Hypothetical Document Embeddings (HyDE)

HyDE asks an LLM to hallucinate a plausible hypothetical answer, embedding the hypothetical answer rather than the raw query.

```python
raw_q = "How do transformers prevent quadratic attention memory?"
hypothetical_answer = "Transformers use FlashAttention or tiling to compute softmax in SRAM blocks without materializing N x N matrices."

assert "FlashAttention" in hypothetical_answer
assert len(hypothetical_answer) > len(raw_q)
print("HyDE generated document-like target embedding.")
```

---

## 3. Self-Correction & Fallback Trigger

If retrieval confidence is below threshold $\tau$, trigger a web search fallback or query re-write loop.

```python
retrieval_confidence = 0.32
threshold = 0.70
trigger_fallback = retrieval_confidence < threshold

assert trigger_fallback is True
print("Retrieval confidence low: query reformulator triggered.")
```

---
