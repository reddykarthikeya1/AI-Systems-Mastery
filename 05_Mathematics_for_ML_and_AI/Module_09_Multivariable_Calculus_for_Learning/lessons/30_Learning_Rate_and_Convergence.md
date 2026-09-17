# Lesson 09.30: Learning Rate and Convergence

## Learning Objectives
- Understand the dynamics of under-stepping, optimal stepping, and overshooting.
- Characterize stable learning rate regimes on 1D quadratics.

## Prerequisites
- 09.29 Gradient Descent: The Update Rule.

---

## 1. The Core Idea
On quadratic $f(x) = \frac{1}{2} a x^2$ with $a > 0$, the update is $x_{t+1} = (1 - \eta a) x_t$.
Convergence occurs if and only if $|1 - \eta a| < 1$, which requires:
$$0 < \eta < \frac{2}{a}$$
- $\eta = 1/a$: exact one-step convergence.
- $1/a < \eta < 2/a$: damped oscillation.
- $\eta > 2/a$: exponential explosion.

---

## 2. Mathematical Exposition & Worked Example
For $f(x) = 5 x^2$ ($a = 10$). Upper stability threshold is $\eta_{\max} = 2/10 = 0.2$.
If $\eta = 0.25$, factor is $|1 - 0.25(10)| = |-1.5| = 1.5 > 1$ (diverges).
If $\eta = 0.1$, factor is $1 - 0.1(10) = 0$ (converges in 1 step).

---

## 3. Verify it in code

```python
import numpy as np
a = 10.0
eta_stable = 0.1
eta_unstable = 0.25

x = 1.0
x = x - eta_stable * (a * x)
assert np.isclose(x, 0.0)

x_div = 1.0
x_div = x_div - eta_unstable * (a * x_div)
assert np.isclose(abs(x_div), 1.5)
```

---

## 4. The mistake people actually make
Believing larger learning rates always train faster; once eta > 2/L, loss immediately explodes to NaN.

---

## Check yourself
1. What is the maximum stable learning rate for f(x) = (1/2) a x^2?
2. What happens if eta = 1/a on a 1D quadratic?

<details>
<summary>Answers</summary>

1. eta < 2 / a.
2. Exact convergence to the minimum in a single step.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [31_Lipschitz_Gradients_and_the_Safe_Step_Size.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\31_Lipschitz_Gradients_and_the_Safe_Step_Size.md)
