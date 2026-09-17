# Lesson 09.41: Mini-Batch Size and the Gradient Noise Scale

## Learning Objectives
- Define the Gradient Noise Scale (GNS): B_{noise} = tr(Sigma) / ||G||^2.
- Determine critical batch sizes for distributed data parallelism.

## Prerequisites
- 09.40 Variance of the Stochastic Gradient.

---

## 1. The Core Idea
The **Gradient Noise Scale** (McCandlish et al., OpenAI) quantifies the signal-to-noise ratio of training:
$$B_{\text{noise}} = \frac{\text{tr}(\boldsymbol{\Sigma})}{\|\mathbf{G}\|^2}$$
- If batch size $B \ll B_{\text{noise}}$: gradients are noise-dominated; increasing $B$ yields linear scaling speedups without wasting compute.
- If $B \gg B_{\text{noise}}$: gradients are signal-dominated; further increasing $B$ yields diminishing returns.

---

## 2. Mathematical Exposition & Worked Example
Let trace of noise covariance $\text{tr}(\boldsymbol{\Sigma}) = 8000$ and squared true gradient norm $\|\mathbf{G}\|^2 = 2.0$.
Critical batch size $B_{\text{noise}} = 8000 / 2.0 = 4000$ tokens/samples.

---

## 3. Verify it in code

```python
import numpy as np
tr_sigma = 8000.0
g_norm_sq = 2.0
b_noise = tr_sigma / g_norm_sq
assert b_noise == 4000.0
```

---

## 4. The mistake people actually make
Scaling batch size into the millions early in training when B_noise is small, wasting compute on redundant gradient evaluations.

---

## Check yourself
1. What is the Gradient Noise Scale formula?
2. What happens when training with batch size B >> B_noise?

<details>
<summary>Answers</summary>

1. B_noise = tr(Sigma) / ||G||^2.
2. Diminishing parallel returns; compute is wasted because gradient variance has already been squashed.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [42_Learning_Rate_Schedules.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\42_Learning_Rate_Schedules.md)
