# Lesson 09.36: RMSProp

## Learning Objectives
- Formulate RMSProp with Exponential Moving Average (EMA): v_{t+1} = gamma v_t + (1-gamma) g_t^2.
- Resolve AdaGrad's learning rate decay problem.

## Prerequisites
- 09.35 AdaGrad.

---

## 1. The Core Idea
**RMSProp** (Hinton) replaces AdaGrad's monotonic accumulation with an **exponential moving average** of squared gradients:
$$v_{t+1} = \gamma v_t + (1 - \gamma) g_t^2, \quad \theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{v_{t+1} + \epsilon}} g_t$$
With $\gamma \approx 0.99$, RMSProp discards ancient gradient history, allowing the effective learning rate to adapt dynamically to the local curvature throughout training.

---

## 2. Mathematical Exposition & Worked Example
$\gamma = 0.9, \eta = 0.01, \epsilon = 1e-8, v_0 = 0$.
Step 1: $g = 10.0 \implies v_1 = 0.1(100) = 10.0$. Step $= \frac{0.01}{\sqrt{10}} 10 \approx 0.0316$.
Step 2: $g = 0.1 \implies v_2 = 0.9(10) + 0.1(0.01) = 9.001$. Step $= \frac{0.01}{\sqrt{9.001}} 0.1 \approx 0.00033$.

---

## 3. Verify it in code

```python
import numpy as np
gamma = 0.9
eta = 0.01
v = 0.0
g1 = 10.0
v1 = gamma * v + (1.0 - gamma) * (g1**2)
step1 = (eta / np.sqrt(v1)) * g1

assert np.isclose(v1, 10.0)
assert np.isclose(step1, (0.01 / np.sqrt(10.0)) * 10.0)
```

---

## 4. The mistake people actually make
Omitting the small epsilon (e.g. 1e-8) in the denominator, causing division by zero when gradients vanish.

---

## Check yourself
1. How does RMSProp fix AdaGrad's premature freezing?
2. What does the parameter gamma control in RMSProp?

<details>
<summary>Answers</summary>

1. By using an exponential moving average of squared gradients instead of an unweighted cumulative sum.
2. The memory horizon (decay rate) of past squared gradients.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [37_Adam_and_Its_Bias_Correction.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\37_Adam_and_Its_Bias_Correction.md)
