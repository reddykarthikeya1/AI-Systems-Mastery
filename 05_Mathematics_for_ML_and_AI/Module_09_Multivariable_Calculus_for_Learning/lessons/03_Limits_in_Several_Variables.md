# Lesson 09.03: Limits in Several Variables

## Learning Objectives
- Understand path-dependent limits in R^n.
- Prove non-existence of a multivariable limit by evaluating along different trajectories.

## Prerequisites
- 09.01 Functions of Several Variables.

---

## 1. The Core Idea
In single-variable calculus, $x \to x_0$ has only two directions (left and right). In $\mathbb{R}^n$, $\mathbf{x} \to \mathbf{x}_0$ along infinitely many continuous paths. For $\lim_{\mathbf{x} \to \mathbf{x}_0} f(\mathbf{x}) = L$ to exist, the limit along **every conceivable trajectory** must equal $L$.

---

## 2. Mathematical Exposition & Worked Example
Consider $f(x, y) = \frac{xy}{x^2 + y^2}$ as $(x, y) \to (0, 0)$. Along $y = mx$: $f(x, mx) = \frac{m x^2}{x^2 + m^2 x^2} = \frac{m}{1 + m^2}$. Since this depends on slope $m$, the limit does not exist!

---

## 3. Verify it in code

```python
import numpy as np
def f(x, y):
    return (x * y) / (x**2 + y**2)

# Path y = x (m = 1): limit is 1/2 = 0.5
val_m1 = f(1e-5, 1e-5)
# Path y = 2x (m = 2): limit is 2/5 = 0.4
val_m2 = f(1e-5, 2e-5)

assert np.isclose(val_m1, 0.5)
assert np.isclose(val_m2, 0.4)
assert not np.isclose(val_m1, val_m2)
```

---

## 4. The mistake people actually make
Testing only the coordinate axes x=0 and y=0 to conclude a limit exists, missing diagonal or parabolic approach paths.

---

## Check yourself
1. How many approach directions exist when taking a limit in R^2?
2. If lim along y=x is 1 and lim along y=2x is 2, does the limit exist?

<details>
<summary>Answers</summary>

1. Infinitely many paths (straight lines, parabolas, spirals, etc.).
2. No, limit existence requires the exact same value along all paths.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [04_Continuity_in_Rn.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\04_Continuity_in_Rn.md)
