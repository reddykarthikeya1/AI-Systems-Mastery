# Lesson 09.42: Learning Rate Schedules

## Learning Objectives
- Implement linear warmup and cosine annealing schedules.
- Explain why warmup stabilizes Adam during early variance estimation.

## Prerequisites
- 09.37 Adam and Its Bias Correction.

---

## 1. The Core Idea
Static learning rates are suboptimal. Modern LLM training universally uses:
1. **Linear Warmup**: $\eta_t = \eta_{\max} \frac{t}{T_{\text{warmup}}}$ for $t \le T_{\text{warmup}}$ (prevents divergent updates while Adam accumulates accurate moment statistics).
2. **Cosine Decay**: $\eta_t = \eta_{\min} + \frac{1}{2}(\eta_{\max} - \eta_{\min}) \left(1 + \cos\left(\frac{t - T_{\text{warmup}}}{T_{\max} - T_{\text{warmup}}} \pi\right)\right)$.

---

## 2. Mathematical Exposition & Worked Example
$\eta_{\max} = 1e-3, \eta_{\min} = 1e-4$, warmup $T_w = 1000$, total $T = 10000$.
At step $t = 500$: $\eta_{500} = 1e-3 \times (500 / 1000) = 5e-4$.
At midpoint $t = 5500$: cosine argument is $\pi/2 \implies \cos(\pi/2) = 0$. $\eta = 1e-4 + 0.5(9e-4)(1 + 0) = 5.5e-4$.

---

## 3. Verify it in code

```python
import numpy as np
def lr_schedule(t, t_w=1000, t_max=10000, lr_max=1e-3, lr_min=1e-4):
    if t < t_w:
        return lr_max * (t / t_w)
    progress = (t - t_w) / (t_max - t_w)
    return lr_min + 0.5 * (lr_max - lr_min) * (1.0 + np.cos(np.pi * progress))

assert np.isclose(lr_schedule(500), 5e-4)
assert np.isclose(lr_schedule(5500), 5.5e-4)
assert np.isclose(lr_schedule(10000), 1e-4)
```

---

## 4. The mistake people actually make
Decaying learning rate to zero too early, freezing parameters before late-stage convergence.

---

## Check yourself
1. Why is warmup crucial when training with Adam?
2. What is the shape of a cosine annealing learning rate curve?

<details>
<summary>Answers</summary>

1. It prevents massive destructive updates during the initial steps when variance estimates are noisy.
2. A smooth half-cosine wave smoothly tapering from lr_max to lr_min.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [43_Newtons_Method.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\43_Newtons_Method.md)
