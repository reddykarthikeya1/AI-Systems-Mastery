# Lesson 09.38: Why Adam Sometimes Fails to Converge

## Learning Objectives
- Analyze Reddi et al.'s non-convergence proof of Adam on convex problems.
- Explain how AMSGrad fixes this via non-decreasing second moment memory: v_max = max(v_max, v_t).

## Prerequisites
- 09.37 Adam and Its Bias Correction.

---

## 1. The Core Idea
In 2018, Reddi et al. proved that Adam can fail to converge even on simple convex online optimization problems.
Root cause: because $v_t$ is an exponential average, $v_t$ can **decrease**, causing the effective step size $\frac{\eta}{\sqrt{v_t}}$ to **increase** unexpectedly when rare informative gradients appear.
**AMSGrad** solves this by enforcing monotonic second moments: $\hat{v}_t = \max(\hat{v}_{t-1}, v_t)$.

---

## 2. Mathematical Exposition & Worked Example
If $v_{t-1} = 10.0$ and current gradient $g_t = 0.1$, $v_t = 0.999(10) + 0.001(0.01) \approx 9.99$.
Under standard Adam, $v$ decreases.
Under AMSGrad, $\hat{v}_t = \max(10.0, 9.99) = 10.0$, preventing harmful step size inflation.

---

## 3. Verify it in code

```python
import numpy as np
v_prev = 10.0
v_curr = 9.99
amsgrad_v = max(v_prev, v_curr)
assert amsgrad_v == 10.0
```

---

## 4. The mistake people actually make
Assuming Adam is globally convergent across all hyperparameter regimes; in practice, learning rate decay and weight decay (AdamW) are essential.

---

## Check yourself
1. Why can the effective step size in Adam unexpectedly increase?
2. How does AMSGrad ensure non-increasing effective step sizes?

<details>
<summary>Answers</summary>

1. Because the second moment v_t can decrease when moving from high-gradient to low-gradient regions.
2. By taking the running maximum: v_hat = max(v_hat_{t-1}, v_t).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [39_Stochastic_Gradient_Descent.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\39_Stochastic_Gradient_Descent.md)
