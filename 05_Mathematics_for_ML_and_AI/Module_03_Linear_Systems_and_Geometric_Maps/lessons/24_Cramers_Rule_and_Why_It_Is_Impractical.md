# Lesson 03.24 — Cramer's Rule and Why It Is Impractical

> **Module 03:** Linear Systems and Geometric Maps · Lesson 24 of 35

---

## What you will be able to do after this lesson

- [ ] Solve small 2x2 systems using Cramer's rule x_i = det(A_i) / det(A).
- [ ] Explain why O((n+1)!) complexity makes Cramer's rule useless for n > 4.

## Prerequisites

- 03.21 Determinants.

---

## 1. The idea

**Cramer's Rule** expresses solutions analytically as $x_i = \frac{\det(A_i)}{\det(A)}$, where $A_i$ replaces column $i$ of $A$ with $\mathbf{b}$. While theoretically elegant, computing $n+1$ determinants takes $O((n+1)!)$ operations via definition or $O(n^4)$ via elimination, far worse than Gaussian elimination ($O(n^3)$).

---

## 2. Worked example

System $x + 2y = 5$, $3x + y = 5$. $\det(A) = 1(1) - 2(3) = -5$. $A_1 = \begin{bmatrix} 5 & 2 \\ 5 & 1 \end{bmatrix}, \det(A_1) = -5 \implies x = -5/-5 = 1$. $A_2 = \begin{bmatrix} 1 & 5 \\ 3 & 5 \end{bmatrix}, \det(A_2) = -10 \implies y = -10/-5 = 2$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0], [3.0, 1.0]])
b = np.array([5.0, 5.0])
detA = np.linalg.det(A)

A1 = A.copy()
A1[:, 0] = b
A2 = A.copy()
A2[:, 1] = b

x = np.linalg.det(A1) / detA
y = np.linalg.det(A2) / detA
assert np.allclose([x, y], [1.0, 2.0])
```

---

## 4. The mistake people actually make

Implementing Cramer's rule in code for large systems. For n = 20, Cramer's rule takes longer than the age of the universe.

---

## Check yourself

1. What is Cramer's formula for variable x_i?
2. What is the computational complexity of Cramer's rule using naive determinants?

<details>
<summary>Answers</summary>

1. x_i = det(A_i) / det(A).
2. O((n + 1)!).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](25_LU_Decomposition.md)
