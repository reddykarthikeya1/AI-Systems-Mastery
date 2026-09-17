# Lesson 09.47: The KKT Conditions

## Learning Objectives
- State the 4 Karush-Kuhn-Tucker (KKT) conditions: Stationarity, Primal Feasibility, Dual Feasibility, and Complementary Slackness.
- Verify KKT conditions on support vector machine (SVM) margins.

## Prerequisites
- 09.46 Lagrange Multipliers.

---

## 1. The Core Idea
For $\min f(\mathbf{x})$ s.t. $g_i(\mathbf{x}) \le 0, h_j(\mathbf{x}) = 0$, the **KKT conditions** are necessary for optimality:
1. **Stationarity**: $\nabla f(\mathbf{x}^*) + \sum \lambda_i^* \nabla g_i(\mathbf{x}^*) + \sum \nu_j^* \nabla h_j(\mathbf{x}^*) = \mathbf{0}$
2. **Primal Feasibility**: $g_i(\mathbf{x}^*) \le 0, \; h_j(\mathbf{x}^*) = 0$
3. **Dual Feasibility**: $\lambda_i^* \ge 0$
4. **Complementary Slackness**: $\lambda_i^* g_i(\mathbf{x}^*) = 0$

---

## 2. Mathematical Exposition & Worked Example
In SVM classification, complementary slackness requires $\alpha_i (y_i(\mathbf{w}^T \mathbf{x}_i + b) - 1) = 0$.
If a point is not on the margin ($y_i(\dots) > 1$), then $\alpha_i = 0$ (does not affect model). Only points strictly on the margin have $\alpha_i > 0$ (**support vectors**)!

---

## 3. Verify it in code

```python
import numpy as np
# Complementary slackness check
alpha = np.array([0.0, 1.5, 0.0])
margin_slack = np.array([0.8, 0.0, 1.2])  # g_i(x)
# Product must be 0 for all i
assert np.allclose(alpha * margin_slack, 0.0)
```

---

## 4. The mistake people actually make
Allowing negative dual multipliers lambda_i < 0 for inequality constraints (violates dual feasibility).

---

## Check yourself
1. What are the four KKT conditions?
2. What does complementary slackness imply for support vector machines?

<details>
<summary>Answers</summary>

1. Stationarity, Primal Feasibility, Dual Feasibility, and Complementary Slackness.
2. Only data points lying strictly on the margin boundary have non-zero alpha_i weights.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [48_Duality_and_the_Dual_Problem.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\48_Duality_and_the_Dual_Problem.md)
