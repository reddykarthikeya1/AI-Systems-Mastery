# Lesson 09.31: Lipschitz Gradients and the Safe Step Size

## Learning Objectives
- Define L-Lipschitz continuous gradients: ||nabla f(x) - nabla f(y)|| <= L ||x - y||.
- Prove the descent lemma: f(x - (1/L) nabla f(x)) <= f(x) - (1/(2L)) ||nabla f(x)||^2.

## Prerequisites
- 09.27 Strong Convexity and Smoothness.

---

## 1. The Core Idea
If $\nabla f$ is $L$-Lipschitz, the **Descent Lemma** provides a guaranteed upper quadratic envelope:
$$f(\mathbf{y}) \le f(\mathbf{x}) + \nabla f(\mathbf{x})^T (\mathbf{y} - \mathbf{x}) + \frac{L}{2}\|\mathbf{y} - \mathbf{x}\|^2$$
Choosing step $\eta \le 1/L$ guarantees monotonic decrease at every iteration:
$$f\left(\mathbf{x} - \frac{1}{L}\nabla f(\mathbf{x})\right) \le f(\mathbf{x}) - \frac{1}{2L}\|\nabla f(\mathbf{x})\|^2$$

---

## 2. Mathematical Exposition & Worked Example
For $f(x) = 2 x^2$, $f''(x) = 4 \implies L = 4$. Safe step is $\eta = 1/4 = 0.25$.
At $x = 2$, $f(2) = 8$, $\nabla f(2) = 8$. Next point: $x - \eta \nabla f = 2 - 0.25(8) = 0$.
Decrease: $f(0) - f(2) = -8 \le -\frac{1}{2(4)}(8^2) = -8$.

---

## 3. Verify it in code

```python
import numpy as np
L = 4.0
eta = 1.0 / L
x = 2.0
f_x = 2.0 * x**2
g_x = 4.0 * x

x_next = x - eta * g_x
f_next = 2.0 * x_next**2
guaranteed_bound = f_x - (1.0 / (2.0 * L)) * (g_x**2)

assert f_next <= guaranteed_bound
assert np.isclose(f_next, 0.0)
```

---

## 4. The mistake people actually make
Assuming all neural network losses have a globally bounded Lipschitz constant L (non-linearities with unbounded curvature violate global L-smoothness).

---

## Check yourself
1. What is the safe step size for an L-smooth objective?
2. By how much is loss guaranteed to decrease per step with eta = 1/L?

<details>
<summary>Answers</summary>

1. eta <= 1 / L.
2. At least (1 / (2L)) * ||nabla f(x)||^2.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [32_Convergence_Rate_on_Convex_Objectives.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\32_Convergence_Rate_on_Convex_Objectives.md)
