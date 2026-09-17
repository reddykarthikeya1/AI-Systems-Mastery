# Lesson 09.04: Continuity in Rn

## Learning Objectives
- Define multivariable continuity: lim_{x -> x_0} f(x) = f(x_0).
- Recognize continuity of polynomials, exponentials, and compositions in neural architectures.

## Prerequisites
- 09.03 Limits in Several Variables.

---

## 1. The Core Idea
A function $f: \mathbb{R}^n \to \mathbb{R}$ is continuous at $\mathbf{x}_0$ if $\lim_{\mathbf{x} \to \mathbf{x}_0} f(\mathbf{x}) = f(\mathbf{x}_0)$. Compositions and sums of continuous functions (e.g. affine layers + sigmoid/GELU activations) remain continuous across their entire domain.

---

## 2. Mathematical Exposition & Worked Example
$f(x, y) = \exp(-(x^2 + y^2))$. As $(x, y) \to (0, 0)$, $-(x^2 + y^2) \to 0$, so $\lim f(x, y) = \exp(0) = 1 = f(0, 0)$. Thus $f$ is continuous everywhere.

---

## 3. Verify it in code

```python
import numpy as np
def f(x, y):
    return np.exp(-(x**2 + y**2))

coords = np.array([[0.01, 0.01], [1e-4, 1e-4], [1e-6, 1e-6]])
vals = [f(x, y) for x, y in coords]
assert np.isclose(f(0.0, 0.0), 1.0)
assert np.allclose(vals[-1], 1.0, atol=1e-5)
```

---

## 4. The mistake people actually make
Assuming piecewise activation functions like ReLU are discontinuous; ReLU is continuous everywhere, though not differentiable at 0.

---

## Check yourself
1. Is f(x) = max(0, x) (ReLU) continuous at x = 0?
2. What happens to the product of two continuous multivariable functions?

<details>
<summary>Answers</summary>

1. Yes, the left and right limits both equal 0 = f(0).
2. The product of continuous functions is guaranteed to be continuous.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [05_Partial_Derivatives.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\05_Partial_Derivatives.md)
