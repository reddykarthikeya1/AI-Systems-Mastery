# Lesson 09.23: The Second Derivative Test in Rn

## Learning Objectives
- Apply the eigenvalue test: H > 0 (local min), H < 0 (local max), indefinite (saddle).
- Evaluate determinants and eigenvalues to determine definiteness.

## Prerequisites
- 09.22 Critical Points and Their Classification.

---

## 1. The Core Idea
At a critical point $\nabla f(\mathbf{x}^*) = \mathbf{0}$:
1. $\mathbf{H} \succ 0$ (all $\lambda_i > 0$): **Strict Local Minimum**
2. $\mathbf{H} \prec 0$ (all $\lambda_i < 0$): **Strict Local Maximum**
3. $\mathbf{H}$ indefinite (some $\lambda_i > 0$, some $\lambda_j < 0$): **Saddle Point**
4. If $\det(\mathbf{H}) = 0$ with no opposing signs: Test is inconclusive.

---

## 2. Mathematical Exposition & Worked Example
Hessian at $(0, 0)$ is $\mathbf{H} = \begin{bmatrix} 4 & 1 \\ 1 & 3 \end{bmatrix}$.
Eigenvalues: $\det(\mathbf{H} - \lambda \mathbf{I}) = (4-\lambda)(3-\lambda) - 1 = \lambda^2 - 7\lambda + 11 = 0$.
$\lambda = \frac{7 \pm \sqrt{49 - 44}}{2} = \frac{7 \pm \sqrt{5}}{2} > 0$. Both positive $\implies$ strict local minimum.

---

## 3. Verify it in code

```python
import numpy as np
H = np.array([[4.0, 1.0], [1.0, 3.0]])
eigvals = np.linalg.eigvalsh(H)
assert np.all(eigvals > 0)  # Positive definite -> local minimum
```

---

## 4. The mistake people actually make
Claiming a point is a local minimum when some eigenvalues are zero without checking higher-order terms.

---

## Check yourself
1. What does H > 0 (positive definite) imply for a critical point?
2. What if H has both positive and negative eigenvalues?

<details>
<summary>Answers</summary>

1. Strict local minimum.
2. It is a saddle point.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [24_Saddle_Points_and_Why_Deep_Networks_Have_Many.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\24_Saddle_Points_and_Why_Deep_Networks_Have_Many.md)
