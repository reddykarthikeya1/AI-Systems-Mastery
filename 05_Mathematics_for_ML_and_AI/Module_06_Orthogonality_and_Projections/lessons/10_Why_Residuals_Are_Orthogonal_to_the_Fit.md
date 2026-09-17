# Lesson 06.10 — Why Residuals Are Orthogonal to the Fit

> **Module 06:** Orthogonality and Projections · Lesson 10 of 18

---

## What you will be able to do after this lesson

- [ ] Prove A^T e = 0 for residual e = b - A x_hat.
- [ ] Decompose total sum of squares TSS = ESS + RSS.

## Prerequisites

- 06.09 Least Squares as Projection.

---

## 1. The idea

The residual $\mathbf{e} = \mathbf{b} - A\hat{\mathbf{x}}$ is perpendicular to the fitted space: $A^T \mathbf{e} = \mathbf{0}$. Therefore $\hat{\mathbf{y}} \cdot \mathbf{e} = (A\hat{\mathbf{x}})^T \mathbf{e} = \hat{\mathbf{x}}^T (A^T \mathbf{e}) = 0$. By Pythagorean theorem, $\|\mathbf{b}\|^2 = \|\hat{\mathbf{y}}\|^2 + \|\mathbf{e}\|^2$ (TSS = ESS + RSS).

---

## 2. Worked example

Using the previous fit: $\hat{\mathbf{y}} = [7/6, 10/6, 13/6]^T$. Residual $\mathbf{e} = \mathbf{b} - \hat{\mathbf{y}} = [-1/6, 2/6, -1/6]^T$. Dot product $\hat{\mathbf{y}} \cdot \mathbf{e} = -\frac{7}{36} + \frac{20}{36} - \frac{13}{36} = 0$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 0.0], [1.0, 1.0], [1.0, 2.0]])
b = np.array([1.0, 2.0, 2.0])
x_hat = np.linalg.lstsq(A, b, rcond=None)[0]
y_hat = A @ x_hat
e = b - y_hat
assert np.isclose(np.dot(y_hat, e), 0.0)
assert np.allclose(A.T @ e, [0.0, 0.0])
assert np.isclose(np.linalg.norm(b)**2, np.linalg.norm(y_hat)**2 + np.linalg.norm(e)**2)
```

---

## 4. The mistake people actually make

Assuming residuals sum to zero even when no intercept (constant bias column) is included in A.

---

## Check yourself

1. Is the residual vector orthogonal to every feature column in A?
2. When is sum(e_i) == 0 guaranteed?

<details>
<summary>Answers</summary>

1. Yes, A^T e = 0 ensures orthogonality to every column.
2. Only when a column of ones (bias/intercept) is included in A.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](11_GramSchmidt_Orthogonalization.md)
