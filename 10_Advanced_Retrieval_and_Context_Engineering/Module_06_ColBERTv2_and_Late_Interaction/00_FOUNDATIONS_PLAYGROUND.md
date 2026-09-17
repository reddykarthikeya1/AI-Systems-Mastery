# 🐣 Interactive Foundations Playground: ColBERTv2 & Late Interaction

> *"Late interaction preserves every token vector until the very end, computing fast MaxSim alignments."*

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

## 1. ColBERT Token-Level MaxSim Scoring

ColBERT computes the sum of maximum cosine similarities for each query token vector across all document token vectors: $\text{Score} = \sum_{i \in Q} \max_{j \in D} (E_{q_i} \cdot E_{d_j})$.

```python
# 2 query tokens, 3 document tokens (1D scalars for illustration)
E_q = [1.0, 0.5]
E_d = [0.2, 0.9, 0.4]

max_sim_q0 = max(E_q[0] * d for d in E_d)  # 1.0 * 0.9 = 0.9
max_sim_q1 = max(E_q[1] * d for d in E_d)  # 0.5 * 0.9 = 0.45
colbert_score = max_sim_q0 + max_sim_q1

assert max_sim_q0 == 0.9
assert max_sim_q1 == 0.45
assert colbert_score == 1.35
print(f"ColBERT MaxSim score: {colbert_score:.2f}")
```

---

## 2. Late Interaction vs Single-Vector Bottleneck

Single dense embeddings crush an entire 500-word passage into one 768-dim vector; ColBERT stores token-level vectors, preserving fine-grained facts.

```python
doc_tokens = 128
emb_dim = 128
colbert_matrix_shape = (doc_tokens, emb_dim)
dense_vector_shape = (1, emb_dim)

assert colbert_matrix_shape[0] == 128
assert dense_vector_shape[0] == 1
print(f"ColBERT preserves {doc_tokens} distinct token vectors per passage.")
```

---

## 3. Residual Vector Quantization Compression

ColBERTv2 compresses each 128-dim token vector to just 16-32 bytes using residual centroid quantization.

```python
raw_bytes = emb_dim * 2  # FP16 = 256 bytes
compressed_bytes = 20    # 20 bytes in ColBERTv2
compression_ratio = raw_bytes / compressed_bytes

assert compression_ratio > 10.0
assert round(compression_ratio, 1) == 12.8
print(f"ColBERTv2 achieves {compression_ratio:.1f}x compression on token vectors.")
```

---
