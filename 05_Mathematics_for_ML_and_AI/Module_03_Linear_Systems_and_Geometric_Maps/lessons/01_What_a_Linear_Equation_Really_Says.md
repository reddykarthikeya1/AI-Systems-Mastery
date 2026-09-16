# Lesson 03.01 — What a Linear Equation Really Says

> **Module 03:** Linear Systems and Geometric Maps · Lesson 1 of 35

---

## What you will be able to do after this lesson

- [ ] State what geometric object a single linear equation defines in R^2 and R^n, and explain the physical meaning of its normal vector.
- [ ] Compute the signed perpendicular distance from any arbitrary point to a decision hyperplane by hand and verify it using NumPy vector operations.

## Prerequisites

- High-school algebra and basic vector arithmetic (inner products).

---

## 1. The idea

A linear equation is usually introduced as an algebraic formula:
$$a_1 x_1 + a_2 x_2 + \dots + a_n x_n = b$$

In machine learning and linear algebra, this view hides the geometric truth. A linear equation is an **inner product constraint**:
$$\mathbf{a}^T \mathbf{x} = b$$

This single statement asserts three profound geometric facts:
1. **The vector $\mathbf{a} = [a_1, \dots, a_n]^T$ is the normal vector**: it points strictly perpendicular to the solution surface.
2. **The constant $b$ controls translation**: it sets how far the surface is shifted away from the origin along the direction of $\mathbf{a}$.
3. **The solution set is a hyperplane**: in 2D it is a line ($2-1=1$ dimension), in 3D it is a flat plane ($3-1=2$ dimensions), and in $\mathbb{R}^n$ it is an $(n-1)$-dimensional subspace translated by an offset.

In binary linear classification (logistic regression, support vector machines), the decision boundary is precisely a single linear equation: $\mathbf{w}^T \mathbf{x} + b = 0$. Every training example $\mathbf{x}$ lies on one side (positive dot product) or the other (negative dot product).

---

## 2. Worked example

Consider the linear equation in $\mathbb{R}^2$:
$$3 x_1 + 4 x_2 = 12$$

### Finding the normal vector and unit normal
The coefficient vector is $\mathbf{a} = [3, 4]^T$.
Its Euclidean norm is:
$$\|\mathbf{a}\|_2 = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = 5$$

The unit normal vector pointing perpendicular to the line is:
$$\mathbf{u} = \frac{\mathbf{a}}{\|\mathbf{a}\|} = \left[ \frac{3}{5}, \frac{4}{5} \right]^T = [0.6, 0.8]^T$$

### Perpendicular distance from origin to line
Divide the entire equation by $\|\mathbf{a}\| = 5$:
$$0.6 x_1 + 0.8 x_2 = \frac{12}{5} = 2.4$$

The perpendicular distance from the origin $(0, 0)$ to the line is exactly $d_0 = 2.4$.

### Checking a point off the line
Take the point $\mathbf{p} = (2, 4)$.
Evaluating the left-hand side:
$$3(2) + 4(4) = 6 + 16 = 22$$
Since $22 > 12$, $\mathbf{p}$ lies in the positive half-space.
The perpendicular distance from $\mathbf{p}$ to the line is:
$$d(\mathbf{p}) = \frac{\mathbf{a}^T \mathbf{p} - b}{\|\mathbf{a}\|} = \frac{22 - 12}{5} = \frac{10}{5} = 2.0$$

---

## 3. Verify it in code

```python
import numpy as np

# Normal vector and constant offset
a = np.array([3.0, 4.0])
b = 12.0

# 1. Norm and unit normal vector
norm_a = np.linalg.norm(a)
assert np.isclose(norm_a, 5.0)

u = a / norm_a
assert np.isclose(np.linalg.norm(u), 1.0)
assert np.allclose(u, [0.6, 0.8])

# 2. Origin distance
dist_origin = b / norm_a
assert np.isclose(dist_origin, 2.4)

# 3. Two points on the line: (4, 0) and (0, 3)
p1 = np.array([4.0, 0.0])
p2 = np.array([0.0, 3.0])
assert np.isclose(np.dot(a, p1), b)
assert np.isclose(np.dot(a, p2), b)

# The vector along the line (p2 - p1) must be strictly orthogonal to the normal vector a
tangent_vector = p2 - p1
assert np.isclose(np.dot(a, tangent_vector), 0.0), "Line direction is orthogonal to normal"

# 4. Point distance off the line
p = np.array([2.0, 4.0])
signed_dist = (np.dot(a, p) - b) / norm_a
assert np.isclose(signed_dist, 2.0)

# Project p onto the line: p_proj = p - signed_dist * u
p_proj = p - signed_dist * u
assert np.isclose(np.dot(a, p_proj), b), "Projected point lies on the line"
```

---

## 4. The mistake people actually make

The most common misconception is confusing the **normal vector** with the **direction of the line**.
When beginners see $3x + 4y = 12$, they intuitively assume the vector $[3, 4]^T$ is parallel to the line.
In reality, $[3, 4]^T$ is orthogonal (perpendicular, at $90^\circ$) to the line.
A vector parallel to the line in 2D is $[-4, 3]^T$ because $[3, 4] \cdot [-4, 3] = -12 + 12 = 0$.
In higher dimensions (e.g. 512-dimensional embedding space in a transformer), a hyperplane has one normal direction but 511 orthogonal directions forming the tangent subspace.

---

## Check yourself

1. What is the perpendicular distance from the origin to the plane $2x_1 - 2x_2 + x_3 = 9$ in R^3?
2. If two linear equations have normal vectors that are scalar multiples of each other, what is the geometric relationship between their hyperplanes?

<details>
<summary>Answers</summary>

1. The normal vector is $\mathbf{a} = [2, -2, 1]^T$. Its norm is $\|\mathbf{a}\| = \sqrt{2^2 + (-2)^2 + 1^2} = \sqrt{4 + 4 + 1} = 3$. The distance from the origin is $b / \|\mathbf{a}\| = 9 / 3 = 3.0$.
2. The hyperplanes are parallel. If the normalized constant offsets $b_1/\|\mathbf{a}_1\| = b_2/\|\mathbf{a}_2\|$ are also equal, the equations define the exact same hyperplane; otherwise, they never intersect.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Systems_of_Linear_Equations.md)
