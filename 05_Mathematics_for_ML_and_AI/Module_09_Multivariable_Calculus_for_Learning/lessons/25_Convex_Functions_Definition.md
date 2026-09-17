# Lesson 09.25: Convex Functions Definition

## Learning Objectives
- Define convex functions via chord inequality: f(theta x + (1-theta) y) <= theta f(x) + (1-theta) f(y).
- Recognize that every local minimum of a convex function is a global minimum.

## Prerequisites
- 09.01 Functions of Several Variables.

---

## 1. The Core Idea
A function $f: \mathbb{R}^n \to \mathbb{R}$ is **convex** on a convex domain if for all $\mathbf{x}, \mathbf{y}$ and $\theta \in [0, 1]$:
$$f(\theta \mathbf{x} + (1-\theta) \mathbf{y}) \le \theta f(\mathbf{x}) + (1-\theta) f(\mathbf{y})$$
Geometrically, the line segment (chord) connecting $(\mathbf{x}, f(\mathbf{x}))$ and $(\mathbf{y}, f(\mathbf{y}))$ lies on or above the graph of $f$.

---

## 2. Mathematical Exposition & Worked Example
For $f(x) = x^2$ with $x = 2, y = 6, \theta = 0.5$:
Midpoint $\theta x + (1-\theta)y = 4$. $f(4) = 16$.
Chord height: $0.5 f(2) + 0.5 f(6) = 0.5(4) + 0.5(36) = 20$.
Since $16 \le 20$, the convexity inequality holds.

---

## 3. Verify it in code

```python
import numpy as np
def f(x):
    return x**2

x, y = 2.0, 6.0
theta = 0.5
lhs = f(theta * x + (1.0 - theta) * y)
rhs = theta * f(x) + (1.0 - theta) * f(y)

assert lhs <= rhs
assert np.isclose(lhs, 16.0)
assert np.isclose(rhs, 20.0)
```

---

## 4. The mistake people actually make
Confusing concave and convex functions (a concave function satisfies f(theta x + (1-theta) y) >= theta f(x) + (1-theta) f(y)).

---

## Check yourself
1. What is the defining geometric property of a convex function?
2. What is special about local minima of convex functions?

<details>
<summary>Answers</summary>

1. The line segment connecting any two points on the graph lies above or on the graph.
2. Every local minimum is guaranteed to be a global minimum.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [26_First_and_SecondOrder_Convexity_Tests.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\26_First_and_SecondOrder_Convexity_Tests.md)
