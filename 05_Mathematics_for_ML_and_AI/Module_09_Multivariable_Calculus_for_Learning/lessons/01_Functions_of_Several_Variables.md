# Lesson 09.01: Functions of Several Variables

## Learning Objectives
- Define scalar and vector fields f: R^n -> R and f: R^n -> R^m.
- Understand loss functions as mappings from high-dimensional parameter spaces to scalar losses.

## Prerequisites
- 04.01 Vector Spaces.

---

## 1. The Core Idea
A **function of several variables** maps an input vector $\mathbf{x} \in \mathbb{R}^n$ to an output. In supervised learning, the loss function $L(\mathbf{w})$ maps millions of network weights $\mathbf{w} \in \mathbb{R}^D$ to a single real scalar $L \in \mathbb{R}$ quantifying prediction error.

---

## 2. Mathematical Exposition & Worked Example
Let $f(x, y) = x^2 + 3xy + 2y^2$. At $(x, y) = (2, -1)$, $f(2, -1) = 2^2 + 3(2)(-1) + 2(-1)^2 = 4 - 6 + 2 = 0$.

---

## 3. Verify it in code

```python
import numpy as np
def f(x, y):
    return x**2 + 3*x*y + 2*y**2

val = f(2.0, -1.0)
assert np.isclose(val, 0.0)
assert np.isclose(f(1.0, 1.0), 6.0)
```

---

## 4. The mistake people actually make
Treating multivariable functions as a sequence of independent 1D functions, ignoring coupling interaction terms like xy.

---

## Check yourself
1. What is the domain and codomain of a standard ML loss function?
2. What is the value of f(x, y) = x^2 + y^2 at (3, 4)?

<details>
<summary>Answers</summary>

1. Domain is R^D (parameter space); codomain is R (scalar loss).
2. 3^2 + 4^2 = 25.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [02_Level_Sets_and_Contour_Plots.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\02_Level_Sets_and_Contour_Plots.md)
