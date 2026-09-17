# Lesson 09.02: Level Sets and Contour Plots

## Learning Objectives
- Define level sets {x in R^n : f(x) = c}.
- Interpret contour curves as slices of the loss landscape.

## Prerequisites
- 09.01 Functions of Several Variables.

---

## 1. The Core Idea
A **level set** (or contour line in 2D) of $f: \mathbb{R}^n \to \mathbb{R}$ is the locus of points where the function takes a constant value: $S_c = \{\mathbf{x} \in \mathbb{R}^n : f(\mathbf{x}) = c\}$. In optimization, gradient vectors are always orthogonal to these level sets.

---

## 2. Mathematical Exposition & Worked Example
For $f(x, y) = x^2 + 4y^2 = 16$, the level curve is an ellipse with semi-major axis $a = 4$ along the x-axis and semi-minor axis $b = 2$ along the y-axis.

---

## 3. Verify it in code

```python
import numpy as np
def f(x, y):
    return x**2 + 4.0 * y**2

# Point on level set c = 16
assert np.isclose(f(4.0, 0.0), 16.0)
assert np.isclose(f(0.0, 2.0), 16.0)
assert np.isclose(f(np.sqrt(8.0), np.sqrt(2.0)), 16.0)
```

---

## 4. The mistake people actually make
Assuming gradient vectors are tangent to contour curves; they are strictly orthogonal (perpendicular) to level sets.

---

## Check yourself
1. What geometric shape is the level set x^2 + y^2 = r^2?
2. Why are contour lines closer together in regions of steep slope?

<details>
<summary>Answers</summary>

1. A circle of radius r centered at the origin.
2. Because the function value changes by a fixed delta over a much smaller physical distance.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [03_Limits_in_Several_Variables.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\03_Limits_in_Several_Variables.md)
