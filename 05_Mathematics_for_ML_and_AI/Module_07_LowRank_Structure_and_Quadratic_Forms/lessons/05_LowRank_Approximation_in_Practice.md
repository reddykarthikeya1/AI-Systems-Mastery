# Lesson 07.05 — Low-Rank Approximation in Practice

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 5 of 12

---

## What you will be able to do after this lesson

- [ ] Compute compression ratio and energy retention (explained variance) of low-rank factors.
- [ ] Implement low-rank factorization in LoRA (Low-Rank Adaptation) style.

## Prerequisites

- 07.04 Truncated SVD.

---

## 1. The idea

Storing an $m \times n$ matrix takes $m \cdot n$ floats. Its rank-$k$ factorization $U_k \Sigma_k V_k^T$ requires only $k(m + n + 1)$ parameters. When $k \ll \min(m, n)$, this saves massive memory and compute (the foundation of LoRA in LLMs).

---

## 2. Worked example

For $m=1000, n=1000$, full matrix has $1,000,000$ params. A rank-16 approximation needs $16(1000 + 1000) = 32,000$ params (96.8% reduction).

---

## 3. Verify it in code

```python
import numpy as np

m, n, k = 100, 100, 5
np.random.seed(42)
A = np.random.randn(m, n)
U, s, Vt = np.linalg.svd(A)

# Explained variance ratio
variance_retained = np.sum(s[:k]**2) / np.sum(s**2)
assert 0.0 < variance_retained < 1.0

# LoRA parameter reduction
full_params = m * n
low_rank_params = k * (m + n)
assert low_rank_params < full_params
```

---

## 4. The mistake people actually make

Choosing rank k too small when singular values decay slowly, losing critical signal.

---

## Check yourself

1. How is the explained variance ratio computed from singular values?
2. How does LoRA represent weight updates?

<details>
<summary>Answers</summary>

1. sum_{i=1}^k sigma_i^2 / sum_{all} sigma_j^2.
2. As Delta W = B @ A where B is (d, r) and A is (r, k) with r << min(d, k).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](06_The_MoorePenrose_Pseudoinverse.md)
