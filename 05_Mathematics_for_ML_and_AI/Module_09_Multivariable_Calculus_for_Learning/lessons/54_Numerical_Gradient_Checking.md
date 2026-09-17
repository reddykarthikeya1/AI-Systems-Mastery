# Lesson 09.54: Numerical Gradient Checking

## Learning Objectives
- Implement two-sided central finite differences: (f(x + h) - f(x - h)) / (2h).
- Evaluate relative error: ||g_num - g_ana|| / (||g_num|| + ||g_ana||).

## Prerequisites
- 09.05 Partial Derivatives.

---

## 1. The Core Idea
To verify custom autograd backward implementations, **numerical gradient checking** computes central differences:
$$\frac{\partial f}{\partial x_i} \approx \frac{f(\mathbf{x} + h \mathbf{e}_i) - f(\mathbf{x} - h \mathbf{e}_i)}{2h}$$
Central difference error is $O(h^2)$ (far superior to forward difference $O(h)$). A typical test passes if relative error $< 10^{-6}$ for float64 precision.

---

## 2. Mathematical Exposition & Worked Example
For $f(x) = x^3$ at $x = 2$: $f'(2) = 12.0$.
Central difference with $h = 10^{-4}$:
$\frac{(2.0001)^3 - (1.9999)^3}{2 \times 10^{-4}} = \frac{8.00120006 - 7.99879994}{0.0002} = \frac{0.00240012}{0.0002} = 12.00000001$.

---

## 3. Verify it in code

```python
import numpy as np
def f(x):
    return x[0]**3 + 2.0 * x[1]**2

x = np.array([2.0, 3.0])
g_analytical = np.array([3.0 * x[0]**2, 4.0 * x[1]])
h = 1e-5

g_numerical = np.zeros_like(x)
for i in range(len(x)):
    x_plus = x.copy()
    x_minus = x.copy()
    x_plus[i] += h
    x_minus[i] -= h
    g_numerical[i] = (f(x_plus) - f(x_minus)) / (2.0 * h)

rel_error = np.linalg.norm(g_numerical - g_analytical) / (
    np.linalg.norm(g_numerical) + np.linalg.norm(g_analytical)
)
assert rel_error < 1e-7
```

---

## 4. The mistake people actually make
Setting h too small (e.g. 1e-16 in float32), causing disastrous catastrophic cancellation in floating-point subtraction.

---

## Check yourself
1. Why is central difference preferred over one-sided forward difference?
2. What precision level should be used when performing gradient checks?

<details>
<summary>Answers</summary>

1. Central differences have O(h^2) truncation error compared to O(h) for forward differences.
2. float64 (double precision) with h around 1e-5 to 1e-7.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [55_Automatic_Differentiation_Pitfalls.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\55_Automatic_Differentiation_Pitfalls.md)
