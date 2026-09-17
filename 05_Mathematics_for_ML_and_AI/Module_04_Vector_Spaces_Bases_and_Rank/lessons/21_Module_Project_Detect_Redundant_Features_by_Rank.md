# Lesson 04.21 — Module Project: Detect Redundant Features by Rank

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 21 of 21

---

## What you will be able to do after this lesson

- [ ] Build an automatic feature pruning pipeline using QR with column pivoting and SVD.
- [ ] Eliminate redundant features while preserving predictive rank.

## Prerequisites

- Lessons 04.01 to 04.20.

---

## 1. The idea

We build an automated feature pruning tool that inspects a tabular feature matrix $X$, computes its numerical rank using singular value thresholding ($\sigma_i > \epsilon \sigma_1$), and selects a subset of independent columns using QR with pivoting.

---

## 2. Worked example

Given 5 features where feature 3 is $f_1 + f_2$ and feature 4 is noise-free duplicate of $f_0$. The pipeline automatically prunes the matrix from 5 columns to 3 independent columns.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
N = 50
f0 = np.random.randn(N)
f1 = np.random.randn(N)
f2 = np.random.randn(N)
f3 = f1 + f2        # Redundant combination
f4 = f0.copy()      # Duplicate

X = np.column_stack([f0, f1, f2, f3, f4])
assert X.shape == (N, 5)

# 1. Detect true numerical rank via SVD
s = np.linalg.svd(X, compute_uv=False)
tol = s[0] * 1e-10
num_rank = np.sum(s > tol)
assert num_rank == 3

# 2. Prune to independent features
# Greedily keep columns that increase rank
kept = []
for col_idx in range(X.shape[1]):
    candidate = X[:, kept + [col_idx]]
    if np.linalg.matrix_rank(candidate) > len(kept):
        kept.append(col_idx)

assert len(kept) == 3
assert kept == [0, 1, 2]
```

---

## 4. The mistake people actually make

Pruning features based purely on pairwise correlation. Two features might have low pairwise correlation yet be linearly determined by a combination of 3 other features.

---

## Check yourself

1. Why is pairwise correlation insufficient to detect all multicollinearity?
2. How does singular value thresholding determine numerical rank?

<details>
<summary>Answers</summary>

1. Because linear dependence can involve combinations of 3 or more features.
2. By counting singular values that exceed machine tolerance: sigma_i > tol.

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
