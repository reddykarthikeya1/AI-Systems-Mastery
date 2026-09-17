# Lesson 09.56: Line Search and Trust Regions

## Learning Objectives
- Implement backtracking line search with Armijo condition.
- Formulate trust region constraints: min m_k(p) s.t. ||p|| <= Delta_k.

## Prerequisites
- 09.31 Lipschitz Gradients and the Safe Step Size.

---

## 1. The Core Idea
Instead of static learning rates:
1. **Backtracking Line Search**: Iteratively shrink $\eta \leftarrow \tau \eta$ until the **Armijo condition** is satisfied:
$$f(\mathbf{x}_t - \eta \nabla f(\mathbf{x}_t)) \le f(\mathbf{x}_t) - c \eta \|\nabla f(\mathbf{x}_t)\|^2 \quad (c \in (0, 1))$$
2. **Trust Region Methods**: Approximate $f$ by a quadratic model $m_k(\mathbf{p})$ inside a radius $\|\mathbf{p}\| \le \Delta_k$, expanding or contracting $\Delta_k$ based on how well model predictions match reality.

---

## 2. Mathematical Exposition & Worked Example
For $f(x) = x^2$ at $x = 2$, $f(2) = 4, \nabla f(2) = 4, \|\nabla f\|^2 = 16$.
Armijo condition with $c = 0.1$: $f(2 - 4\eta) \le 4 - 1.6\eta$.
Try $\eta = 1.0$: $f(-2) = 4 \le 4 - 1.6 = 2.4$ (False).
Backtrack $\eta = 0.5$: $f(0) = 0 \le 4 - 0.8 = 3.2$ (True! Accept step $\eta = 0.5$).

---

## 3. Verify it in code

```python
import numpy as np
def f(x): return x**2
def df(x): return 2.0 * x

x = 2.0
c = 0.1
tau = 0.5
eta = 1.0

fx = f(x)
gx = df(x)

while f(x - eta * gx) > fx - c * eta * (gx**2):
    eta *= tau

assert eta == 0.5
assert f(x - eta * gx) == 0.0
```

---

## 4. The mistake people actually make
Setting Armijo parameter c too high (e.g. c > 0.5), which can exclude the true minimum.

---

## Check yourself
1. What is the Armijo sufficient decrease condition?
2. How does a trust region method adjust its radius Delta?

<details>
<summary>Answers</summary>

1. f(x - eta * g) <= f(x) - c * eta * ||g||^2.
2. It expands Delta if the quadratic model accurately predicts the true decrease, and contracts Delta if predictions diverge.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [57_Module_Project_Optimizers_From_Scratch_Benchmarked.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\57_Module_Project_Optimizers_From_Scratch_Benchmarked.md)
