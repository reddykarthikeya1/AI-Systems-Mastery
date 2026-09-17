# Lesson 09.44: Quasi-Newton Methods and L-BFGS

## Learning Objectives
- Understand the BFGS secant equation: B_{k+1} s_k = y_k.
- Explain why Limited-memory BFGS (L-BFGS) stores only the last m vector pairs (s, y).

## Prerequisites
- 09.43 Newton's Method.

---

## 1. The Core Idea
Inverting the $D \times D$ Hessian costs $O(D^3)$ time and $O(D^2)$ space.
**Quasi-Newton methods** (BFGS) build an iterative approximation $\mathbf{B}_{k+1}$ to the Hessian satisfying the secant equation:
$$\mathbf{B}_{k+1} \mathbf{s}_k = \mathbf{y}_k \quad (\mathbf{s}_k = \mathbf{x}_{k+1} - \mathbf{x}_k, \mathbf{y}_k = \nabla f_{k+1} - \nabla f_k)$$
**L-BFGS** stores only the last $m$ displacement pairs $(\mathbf{s}_k, \mathbf{y}_k)$ ($m \approx 5\text{--}20$), reducing memory to $O(m D)$ and computing direction updates via a two-loop recursion.

---

## 2. Mathematical Exposition & Worked Example
In 100,000 dimensions: full Hessian requires $10^{10}$ floats ($40\text{ GB}$).
L-BFGS with history $m = 10$ requires only $2 \times 10 \times 100,000 = 2 \times 10^6$ floats ($8\text{ MB}$), a $5000\times$ reduction!

---

## 3. Verify it in code

```python
import numpy as np
D = 100000
m = 10
full_hessian_elements = D**2
lbfgs_elements = 2 * m * D
savings = full_hessian_elements / lbfgs_elements

assert full_hessian_elements == 10**10
assert lbfgs_elements == 2 * 10**6
assert savings == 5000.0
```

---

## 4. The mistake people actually make
Attempting to use L-BFGS with small stochastic mini-batches; L-BFGS requires highly accurate gradient differences and degrades under stochastic noise.

---

## Check yourself
1. What is the secant equation in Quasi-Newton optimization?
2. Why is L-BFGS preferred over standard BFGS in high dimensions?

<details>
<summary>Answers</summary>

1. B_{k+1} s_k = y_k where s_k = Delta x and y_k = Delta g.
2. It replaces the D x D matrix with a small history buffer of m vectors, scaling linearly in O(mD).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [45_Constrained_Optimization_The_Setup.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\45_Constrained_Optimization_The_Setup.md)
