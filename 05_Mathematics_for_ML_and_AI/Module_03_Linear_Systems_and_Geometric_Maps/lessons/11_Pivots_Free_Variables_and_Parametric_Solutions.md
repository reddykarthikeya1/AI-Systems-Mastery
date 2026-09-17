# Lesson 03.11 — Pivots, Free Variables and Parametric Solutions

> **Module 03:** Linear Systems and Geometric Maps · Lesson 11 of 35

---

## What you will be able to do after this lesson

- [ ] Identify basic (pivot) variables and free variables.
- [ ] Express under-determined solution sets in parametric vector form x = x_p + s v1.

## Prerequisites

- 03.08 RREF.

---

## 1. The idea

In RREF, columns containing pivots correspond to **pivot variables**. Columns without pivots correspond to **free variables** (parameters that can take any value). The general solution is expressed as $\mathbf{x} = \mathbf{x}_p + \sum t_i \mathbf{v}_i$, where $\mathbf{x}_p$ is a particular solution and $\mathbf{v}_i$ span the null space.

---

## 2. Worked example

Equation $x_1 + 2x_2 = 4$. Pivot in col 1, $x_2$ free ($x_2 = t$). General solution: $\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 4 \\ 0 \end{bmatrix} + t \begin{bmatrix} -2 \\ 1 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0]])
b = np.array([4.0])
x_p = np.array([4.0, 0.0])
v_null = np.array([-2.0, 1.0])

# For any parameter t, A @ (x_p + t * v_null) == b
for t in [-5.0, 0.0, 2.5, 10.0]:
    sol = x_p + t * v_null
    assert np.allclose(A @ sol, b)
```

---

## 4. The mistake people actually make

Setting free variables to arbitrary constants and claiming the result is the only solution.

---

## Check yourself

1. How many free variables does an m x n matrix with rank r have?
2. What is the role of x_p in the parametric solution x = x_p + t v?

<details>
<summary>Answers</summary>

1. Exactly n - r free variables.
2. x_p is a particular solution satisfying A x_p = b.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](12_Consistency_and_the_Rank_Condition.md)
