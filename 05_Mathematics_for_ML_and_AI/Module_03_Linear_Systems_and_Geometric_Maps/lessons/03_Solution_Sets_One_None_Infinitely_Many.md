# Lesson 03.03 — Solution Sets: One, None, Infinitely Many

> **Module 03:** Linear Systems and Geometric Maps · Lesson 3 of 35

---

## What you will be able to do after this lesson

- [ ] Classify any linear system into having exactly one solution, no solution (inconsistent), or infinitely many solutions (underdetermined) using matrix rank.
- [ ] Verify the Rouché–Capelli theorem in Python by comparing the rank of the coefficient matrix $\text{rank}(A)$ against the augmented matrix $\text{rank}([A|\mathbf{b}])$.

## Prerequisites

- Lesson 03.02: Systems of Linear Equations.

---

## 1. The idea

A system of linear equations $A\mathbf{x} = \mathbf{b}$ never has "two solutions" or "five solutions". For any linear system over real numbers, there are **strictly three possibilities**:

1. **Exactly One Unique Solution**:
   The hyperplanes intersect at a single point.
   Condition: $\text{rank}(A) = \text{rank}([A|\mathbf{b}]) = n$ (where $n$ is the number of variables).

2. **No Solution (Inconsistent)**:
   The constraints contradict each other (e.g. parallel lines that never meet).
   Condition: $\text{rank}(A) < \text{rank}([A|\mathbf{b}])$. The target vector $\mathbf{b}$ lies outside the column space of $A$.

3. **Infinitely Many Solutions (Underdetermined / Dependent)**:
   The constraints are redundant, leaving free degrees of freedom (e.g. two equations representing the exact same line, or 2 equations with 3 unknowns).
   Condition: $\text{rank}(A) = \text{rank}([A|\mathbf{b}]) < n$.

This fundamental trichotomy is formalized by the **Rouché–Capelli Theorem**.

---

## 2. Worked example

### Case 1: Exactly One Solution
$$\begin{aligned}
x_1 + x_2 &= 4 \\
x_1 - x_2 &= 2
\end{aligned}$$
Adding equations yields $2x_1 = 6 \implies x_1 = 3, x_2 = 1$. Unique point $(3, 1)$.
$\text{rank}(A) = 2 = n$.

### Case 2: No Solution (Inconsistent)
$$\begin{aligned}
x_1 + x_2 &= 4 \\
2x_1 + 2x_2 &= 10
\end{aligned}$$
Divide equation (2) by 2: $x_1 + x_2 = 5$.
This asserts $4 = 5$, an impossibility.
The lines are parallel with slopes $-1$ but intercepts $4$ vs $5$.
$\text{rank}(A) = 1$, but $\text{rank}([A|\mathbf{b}]) = 2$. Inconsistent.

### Case 3: Infinitely Many Solutions
$$\begin{aligned}
x_1 + x_2 &= 4 \\
2x_1 + 2x_2 &= 8
\end{aligned}$$
Equation (2) is simply $2 \times$ equation (1).
Any point on the line $x_2 = 4 - x_1$ is a valid solution (e.g. $(4, 0), (0, 4), (2, 2)$).
$\text{rank}(A) = 1 = \text{rank}([A|\mathbf{b}]) < 2$. Free variable parameterizes the solution line.

---

## 3. Verify it in code

```python
import numpy as np

# 1. Unique solution case
A1 = np.array([[1.0, 1.0], [1.0, -1.0]])
b1 = np.array([4.0, 2.0])
aug1 = np.column_stack([A1, b1])

rank_A1 = np.linalg.matrix_rank(A1)
rank_aug1 = np.linalg.matrix_rank(aug1)
assert rank_A1 == 2 and rank_aug1 == 2, "Unique solution: rank(A) == rank([A|b]) == n"
x1 = np.linalg.solve(A1, b1)
assert np.allclose(x1, [3.0, 1.0])

# 2. Inconsistent (no solution) case
A2 = np.array([[1.0, 1.0], [2.0, 2.0]])
b2 = np.array([4.0, 10.0])
aug2 = np.column_stack([A2, b2])

rank_A2 = np.linalg.matrix_rank(A2)
rank_aug2 = np.linalg.matrix_rank(aug2)
assert rank_A2 == 1, "Rows of A2 are linearly dependent"
assert rank_aug2 == 2, "Augmented matrix has higher rank"
assert rank_A2 < rank_aug2, "Inconsistent: rank(A) < rank([A|b])"

# 3. Infinitely many solutions case
A3 = np.array([[1.0, 1.0], [2.0, 2.0]])
b3 = np.array([4.0, 8.0])
aug3 = np.column_stack([A3, b3])

rank_A3 = np.linalg.matrix_rank(A3)
rank_aug3 = np.linalg.matrix_rank(aug3)
assert rank_A3 == 1 and rank_aug3 == 1, "Consistent with free variables: rank(A) == rank([A|b]) < n"

# Test two different points that both satisfy A3 @ x == b3
sol_a = np.array([4.0, 0.0])
sol_b = np.array([2.0, 2.0])
assert np.allclose(A3 @ sol_a, b3)
assert np.allclose(A3 @ sol_b, b3)
```

---

## 4. The mistake people actually make

Beginners assume that whenever a matrix is square ($n \times n$), calling `np.linalg.solve(A, b)` is guaranteed to work.
If the determinant is zero (even due to subtle floating-point collinearity), `np.linalg.solve` will raise a `LinAlgError: Singular matrix`.
In production data pipelines, numerical collinearity occurs routinely when two feature columns are highly correlated (e.g. temperature in Celsius and Fahrenheit). A robust system always inspects matrix condition number and rank before direct inversion.

---

## Check yourself

1. A system has 5 equations and 3 unknowns. What is the maximum possible rank of the coefficient matrix $A$?
2. If $\text{rank}(A) = 3$ for a $5 \times 3$ system, can it have infinitely many solutions?

<details>
<summary>Answers</summary>

1. The maximum rank is $\min(m, n) = \min(5, 3) = 3$.
2. No. If $\text{rank}(A) = 3$, all 3 columns are linearly independent, meaning the null space has dimension $n - \text{rank}(A) = 3 - 3 = 0$. Therefore, the system has either exactly one solution (if $\mathbf{b}$ lies in the column space) or zero solutions (if $\mathbf{b}$ does not lie in the column space). It can never have infinitely many solutions.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](04_Matrices_as_Compact_Notation.md)
