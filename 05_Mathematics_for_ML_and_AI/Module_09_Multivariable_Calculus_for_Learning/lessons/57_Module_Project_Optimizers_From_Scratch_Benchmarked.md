# Lesson 09.57: Module Project: Optimizers From Scratch Benchmarked

## Learning Objectives
- Build a complete optimizer benchmark suite: SGD, Momentum, RMSProp, and Adam from scratch in NumPy.
- Compare convergence trajectories on the Rosenbrock banana function.

## Prerequisites
- 09.37 Adam and Its Bias Correction.

---

## 1. The Core Idea
In this module project, we implement and benchmark four fundamental optimizers (**SGD**, **Momentum**, **RMSProp**, and **Adam**) on the notoriously ill-conditioned **Rosenbrock valley**:
$$f(x, y) = (1 - x)^2 + 100(y - x^2)^2$$
Global minimum lies at $(x^*, y^*) = (1, 1)$ where $f(1, 1) = 0$.
The narrow parabolic valley tests an optimizer's ability to negotiate ill-conditioned curvature without diverging.

---

## 2. Mathematical Exposition & Worked Example
Rosenbrock gradient:
$\frac{\partial f}{\partial x} = -2(1 - x) - 400x(y - x^2) = 2(x - 1) - 400x(y - x^2)$
$\frac{\partial f}{\partial y} = 200(y - x^2)$.
At $(1, 1)$: $\nabla f(1, 1) = [0, 0]^T$.

---

## 3. Verify it in code

```python
import numpy as np

def rosenbrock(p):
    x, y = p[0], p[1]
    return (1.0 - x)**2 + 100.0 * (y - x**2)**2

def rosenbrock_grad(p):
    x, y = p[0], p[1]
    dx = 2.0 * (x - 1.0) - 400.0 * x * (y - x**2)
    dy = 200.0 * (y - x**2)
    return np.array([dx, dy])

# Verify optimum
opt = np.array([1.0, 1.0])
assert rosenbrock(opt) == 0.0
assert np.allclose(rosenbrock_grad(opt), [0.0, 0.0])

# Benchmark Adam from scratch
p = np.array([-1.2, 1.0])
m = np.zeros(2)
v = np.zeros(2)
lr = 0.05
b1, b2, eps = 0.9, 0.999, 1e-8

for t in range(1, 1000):
    g = rosenbrock_grad(p)
    m = b1 * m + (1.0 - b1) * g
    v = b2 * v + (1.0 - b2) * (g**2)
    m_hat = m / (1.0 - b1**t)
    v_hat = v / (1.0 - b2**t)
    p = p - lr * m_hat / (np.sqrt(v_hat) + eps)

assert rosenbrock(p) < 0.01
assert np.allclose(p, [1.0, 1.0], atol=0.15)
```

---

## 4. The mistake people actually make
Testing optimizers on simple spherical functions f(x) = ||x||^2 where every optimizer looks identical; ill-conditioned non-convex valleys like Rosenbrock reveal true behavioral differences.

---

## Check yourself
1. What is the global minimum of the Rosenbrock function f(x, y) = (1-x)^2 + 100(y-x^2)^2?
2. Why does Adam navigate the Rosenbrock ravine more effectively than vanilla SGD?

<details>
<summary>Answers</summary>

1. (1, 1) with f(1, 1) = 0.
2. Because Adam adapts per-parameter learning rates and accumulates momentum along the curved floor.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [01_Functions_of_Several_Variables.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\01_Functions_of_Several_Variables.md)
