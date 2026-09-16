# Lesson 03.02 — Systems of Linear Equations

> **Module 03:** Linear Systems and Geometric Maps · Lesson 2 of 35

---

## What you will be able to do after this lesson

- [ ] Convert any simultaneous system of linear equations between scalar form, row-equation form, matrix form $A\mathbf{x} = \mathbf{b}$, and column-combination form.
- [ ] Compute the solution using both the row picture (intersection point of hyperplanes) and the column picture (linear combination of column vectors) and verify both in NumPy.

## Prerequisites

- Lesson 03.01: What a Linear Equation Really Says.

---

## 1. The idea

A single linear equation restricts an unknown vector to a single hyperplane. A **system of linear equations** is a collection of several such constraints that must hold simultaneously:

$$\begin{aligned}
a_{11} x_1 + a_{12} x_2 + \dots + a_{1n} x_n &= b_1 \\
a_{21} x_1 + a_{22} x_2 + \dots + a_{2n} x_n &= b_2 \\
&\;\vdots \\
a_{m1} x_1 + a_{m2} x_2 + \dots + a_{mn} x_n &= b_m
\end{aligned}$$

There are two equally valid but fundamentally different ways to understand this system:

1. **The Row Picture (Intersection of Hyperplanes)**:
   Each row is a separate constraint. Solving the system means finding the geometric intersection of $m$ hyperplanes in $\mathbb{R}^n$.

2. **The Column Picture (Linear Combination of Vectors)**:
   Group the coefficients by variable rather than by equation:
   $$x_1 \begin{bmatrix} a_{11} \\ a_{21} \\ \vdots \\ a_{m1} \end{bmatrix} + x_2 \begin{bmatrix} a_{12} \\ a_{22} \\ \vdots \\ a_{m2} \end{bmatrix} + \dots + x_n \begin{bmatrix} a_{1n} \\ a_{2n} \\ \vdots \\ a_{mn} \end{bmatrix} = \begin{bmatrix} b_1 \\ b_2 \\ \vdots \\ b_m \end{bmatrix}$$
   In matrix notation: $A\mathbf{x} = \mathbf{b}$.
   Solving the system asks: *What combination of the column vectors of $A$ reconstructs the target vector $\mathbf{b}$?*

The column picture is central to machine learning: feature columns are combined with weights $\mathbf{w}$ to reproduce target outputs $\mathbf{y}$.

---

## 2. Worked example

Consider the 2x2 system:
$$\begin{aligned}
2 x_1 + 1 x_2 &= 5 \\
-1 x_1 + 3 x_2 &= 8
\end{aligned}$$

### In Matrix Form:
$$A = \begin{bmatrix} 2 & 1 \\ -1 & 3 \end{bmatrix}, \quad \mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}, \quad \mathbf{b} = \begin{bmatrix} 5 \\ 8 \end{bmatrix}$$

### Solving by Elimination:
Multiply equation (2) by 2 and add to equation (1):
$$\begin{aligned}
(2 x_1 + x_2) + 2(-x_1 + 3 x_2) &= 5 + 2(8) \\
7 x_2 &= 21 \implies x_2 = 3
\end{aligned}$$
Substitute $x_2 = 3$ into equation (1):
$$2 x_1 + 3 = 5 \implies 2 x_1 = 2 \implies x_1 = 1$$

Solution vector: $\mathbf{x}^* = [1, 3]^T$.

### The Column Picture Verification:
$$1 \begin{bmatrix} 2 \\ -1 \end{bmatrix} + 3 \begin{bmatrix} 1 \\ 3 \end{bmatrix} = \begin{bmatrix} 2 + 3 \\ -1 + 9 \end{bmatrix} = \begin{bmatrix} 5 \\ 8 \end{bmatrix} = \mathbf{b}$$
The target vector $\mathbf{b}$ lies directly in the subspace spanned by the column vectors.

---

## 3. Verify it in code

```python
import numpy as np

# Coefficient matrix A and target vector b
A = np.array([[2.0, 1.0], [-1.0, 3.0]])
b = np.array([5.0, 8.0])

# 1. Direct solution via NumPy
x_star = np.linalg.solve(A, b)
assert np.allclose(x_star, [1.0, 3.0])

# 2. Row picture verification: each row dot product equals b[i]
row_1 = A[0]
row_2 = A[1]
assert np.isclose(np.dot(row_1, x_star), b[0])
assert np.isclose(np.dot(row_2, x_star), b[1])

# 3. Column picture verification: linear combination of columns equals b
col_1 = A[:, 0]
col_2 = A[:, 1]
comb = x_star[0] * col_1 + x_star[1] * col_2
assert np.allclose(comb, b)

# 4. Matrix-vector product identity
assert np.allclose(A @ x_star, b)
```

---

## 4. The mistake people actually make

Learners frequently get trapped exclusively in the row picture because high school algebra teaches equation substitution line by line.
In high-dimensional machine learning (e.g. linear regression with $100,000$ rows and $50$ features), the row picture asks where $100,000$ hyperplanes intersect in $\mathbb{R}^{50}$ (an overdetermined system where no single intersection point exists).
The column picture clarifies everything instantly: we have $50$ column vectors in $\mathbb{R}^{100000}$, and we seek the closest projection in their span to $\mathbf{b}$—which is precisely the least-squares solution.

---

## Check yourself

1. For a system $A\mathbf{x} = \mathbf{b}$ with $A \in \mathbb{R}^{3 \times 2}$, what are the dimensions of the row picture versus the column picture?
2. If the column vectors of $A$ are all parallel to each other, can any arbitrary $\mathbf{b}$ be formed?

<details>
<summary>Answers</summary>

1. Row picture: 3 planes in 2D space $\mathbb{R}^2$ (overdetermined). Column picture: 2 column vectors in 3D space $\mathbb{R}^3$, whose combinations form a 2D plane through the origin.
2. No. If all columns are parallel, their linear combinations only span a 1D line in $\mathbb{R}^m$. Only target vectors $\mathbf{b}$ that lie exactly on that 1D line can be solved.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](03_Solution_Sets_One_None_Infinitely_Many.md)
