# 🐣 Interactive Foundations Playground: Multi-Stage Retrieval & Reranking

> *"Retrieve 100 fast candidates with bi-encoders, then judge the top 10 with a heavy cross-encoder."*

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

## 1. Bi-Encoder vs Cross-Encoder Architecture

Bi-encoders encode query and passage independently ($O(Q) + O(D)$); Cross-encoders feed query and passage together through full cross-attention ($O((Q+D)^2)$).

```python
q_len = 10
d_len = 90
bi_encoder_ops = q_len**2 + d_len**2      # 100 + 8100 = 8200
cross_encoder_ops = (q_len + d_len)**2     # 100^2 = 10,000

assert cross_encoder_ops > bi_encoder_ops
assert cross_encoder_ops == 10_000
print(f"Cross-encoder evaluates all cross-terms: {cross_encoder_ops} attention units.")
```

---

## 2. Top-K Funnel Filtering

The retrieval funnel filters 1,000,000 database chunks down to 100 bi-encoder hits, then down to 5 cross-encoder reranked results.

```python
total_corpus = 1_000_000
stage1_retrieved = 100
stage2_reranked = 5

funnel_ratio = total_corpus / stage2_reranked
assert funnel_ratio == 200_000
assert stage1_retrieved > stage2_reranked
print(f"Retrieval funnel: {total_corpus:,} -> {stage1_retrieved} -> {stage2_reranked} context chunks.")
```

---

## 3. Reranking Score Inversion

Cross-encoders frequently re-order candidates because full cross-attention catches subtle negations.

```python
initial_ranks = ["doc_3", "doc_1", "doc_2"]
reranker_scores = {"doc_1": 0.95, "doc_2": 0.80, "doc_3": 0.20}
final_ranks = sorted(initial_ranks, key=lambda d: reranker_scores[d], reverse=True)

assert final_ranks == ["doc_1", "doc_2", "doc_3"]
assert final_ranks[0] != initial_ranks[0]
print(f"Reranker promoted {final_ranks[0]} to position #1 based on cross-attention score.")
```

---
