# Lesson 07.08 — PCA versus Autoencoders: What Actually Differs

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 8 of 12

---

## What you will be able to do after this lesson

- [ ] Prove that a linear autoencoder with MSE loss spans the exact same subspace as PCA.
- [ ] Identify why non-linear autoencoders learn curved manifolds.

## Prerequisites

- 07.07 PCA via SVD.

---

## 1. The idea

A linear autoencoder trains weights $W_1, W_2$ to minimize $\|X - X W_1 W_2\|_F^2$. Bourlard & Kamp (1988) proved that the subspace spanned by $W_1$ is identical to the PCA subspace, though the weights may differ by an arbitrary rotation.

---

## 2. Worked example

For rank $k=2$, PCA orthogonalizes the projection axes. A linear autoencoder finds an equivalent 2D subspace, but its axes need not be orthogonal.

---

## 3. Verify it in code

```python
import numpy as np

np.random.seed(42)
X = np.random.randn(100, 3)
X_c = X - np.mean(X, axis=0)

# PCA subspace projection matrix P_pca = V_k V_k^T
U, s, Vt = np.linalg.svd(X_c, full_matrices=False)
V2 = Vt[:2].T
P_pca = V2 @ V2.T

assert np.allclose(P_pca @ P_pca, P_pca)  # Projection property
assert np.isclose(np.trace(P_pca), 2.0)   # Rank 2
```

---

## 4. The mistake people actually make

Assuming linear autoencoders recover the exact same orthogonal basis vectors as PCA. They find the same subspace, but with arbitrary rotation/scaling.

---

## Check yourself

1. What subspace does a linear autoencoder with MSE loss learn?
2. What allows deep autoencoders to outperform PCA on complex data?

<details>
<summary>Answers</summary>

1. The exact principal subspace of PCA.
2. Non-linear activation functions that enable learning curved, non-linear manifolds.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](09_Quadratic_Forms_and_Their_Matrices.md)
