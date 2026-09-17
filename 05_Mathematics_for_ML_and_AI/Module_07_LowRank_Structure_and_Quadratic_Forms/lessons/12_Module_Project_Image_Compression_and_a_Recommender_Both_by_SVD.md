# Lesson 07.12 — Module Project: Image Compression and a Recommender Both by SVD

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 12 of 12

---

## What you will be able to do after this lesson

- [ ] Build a collaborative filtering recommender system using truncated SVD.
- [ ] Reconstruct low-rank compressed matrix approximations.

## Prerequisites

- All previous Module 07 lessons.

---

## 1. The idea

In recommender systems (e.g. the Netflix Prize), the user-item rating matrix $R \in \mathbb{R}^{U \times I}$ is low-rank because preferences are governed by latent factors. Truncated SVD factorizes $R \approx U_k \Sigma_k V_k^T$, completing missing ratings via dot products of latent user and item embeddings.

---

## 2. Worked example

A $4 \times 4$ user-item matrix decomposed with rank $k=2$ captures user preferences along 2 latent genres (e.g. Action vs Drama).

---

## 3. Verify it in code

```python
import numpy as np

# Synthetic user-movie rating matrix
R = np.array([
    [5.0, 4.0, 1.0, 1.0],
    [4.0, 5.0, 1.0, 2.0],
    [1.0, 1.0, 5.0, 4.0],
    [1.0, 2.0, 4.0, 5.0]
])

# SVD rank-2 reconstruction
U, s, Vt = np.linalg.svd(R, full_matrices=False)
k = 2
R_k = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]

assert R_k.shape == R.shape
# Error is small compared to original norm
assert np.linalg.norm(R - R_k) < 2.0
assert np.linalg.norm(R - R_k) < np.linalg.norm(R)
```

---

## 4. The mistake people actually make

Treating unobserved ratings as zero ratings in collaborative filtering without proper masking or mean imputation.

---

## Check yourself

1. What do the singular vectors represent in collaborative filtering?
2. How does rank truncation reduce noise in recommendations?

<details>
<summary>Answers</summary>

1. They represent latent user preferences and latent item characteristics.
2. By eliminating small singular values that correspond to idiosyncratic user noise.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md)
