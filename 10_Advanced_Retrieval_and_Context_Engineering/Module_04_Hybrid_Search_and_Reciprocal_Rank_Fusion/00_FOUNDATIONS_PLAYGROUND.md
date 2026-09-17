# 🐣 Interactive Foundations Playground: Hybrid Search & Reciprocal Rank Fusion

> *"Hybrid search marries the precision of keywords (BM25) with the semantic intuition of embeddings."*

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
from collections import defaultdict
```

---

## 1. Reciprocal Rank Fusion (RRF) Formula

RRF combines rankings from dense vector and sparse keyword search: $\text{RRF}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$ with constant $k=60$.

```python
k = 60
# Rank lists (1-indexed)
dense_ranks = {"doc_1": 1, "doc_2": 2, "doc_3": 3}
sparse_ranks = {"doc_2": 1, "doc_1": 3, "doc_4": 2}

rrf_scores = defaultdict(float)
for doc, r in dense_ranks.items():
    rrf_scores[doc] += 1.0 / (k + r)
for doc, r in sparse_ranks.items():
    rrf_scores[doc] += 1.0 / (k + r)

# doc_2: rank 2 dense (1/62) + rank 1 sparse (1/61)
score_doc2 = 1/62 + 1/61
assert abs(rrf_scores["doc_2"] - score_doc2) < 1e-6
best_doc = max(rrf_scores, key=rrf_scores.get)
assert best_doc == "doc_2"
print(f"RRF ranked '{best_doc}' #1 with score {rrf_scores[best_doc]:.5f}")
```

---

## 2. BM25 Term Frequency Saturation

Unlike naive TF, BM25 saturates term frequency impact using $\frac{\text{tf} \cdot (k_1 + 1)}{\text{tf} + k_1}$.

```python
k1 = 1.2
def bm25_tf_weight(tf):
    return (tf * (k1 + 1)) / (tf + k1)

w_1 = bm25_tf_weight(1)
w_10 = bm25_tf_weight(10)
w_100 = bm25_tf_weight(100)

assert w_1 < w_10 < w_100
assert w_100 < k1 + 1  # Bounded by k1 + 1 = 2.2
print(f"BM25 TF weights: tf=1 -> {w_1:.2f}, tf=10 -> {w_10:.2f}, tf=100 -> {w_100:.2f}")
```

---

## 3. Complementary Precision Analysis

Keywords catch exact product SKUs and error codes; vectors catch conceptual semantics.

```python
results_count = len(rrf_scores)
assert results_count == 4
print(f"Fused candidate pool contains {results_count} distinct documents.")
```

---
