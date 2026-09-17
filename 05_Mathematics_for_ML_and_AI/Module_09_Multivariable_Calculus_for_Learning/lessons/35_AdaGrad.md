# Lesson 09.35: AdaGrad

## Learning Objectives
- Formulate AdaGrad: s_{t+1} = s_t + g_t^2, theta_{t+1} = theta_t - (eta / sqrt(s_{t+1} + eps)) g_t.
- Explain why AdaGrad excels for sparse features but stalls on deep architectures.

## Prerequisites
- 09.29 Gradient Descent: The Update Rule.

---

## 1. The Core Idea
**AdaGrad** adapts coordinate learning rates by dividing by the square root of all accumulated squared past gradients:
$$s_{t+1, i} = s_{t, i} + g_{t, i}^2, \quad \theta_{t+1, i} = \theta_{t, i} - \frac{\eta}{\sqrt{s_{t+1, i} + \epsilon}} g_{t, i}$$
Infrequently occurring features receive large updates; frequent features receive small updates. However, because $s_t$ monotonically increases, the effective learning rate decays to zero, prematurely halting training in deep networks.

---

## 2. Mathematical Exposition & Worked Example
Initial $s_0 = 0, \eta = 1.0, \epsilon = 1e-8$.
Step 1: $g = 2.0 \implies s_1 = 4.0$, update $= - (1.0 / \sqrt{4}) 2.0 = -1.0$.
Step 2: $g = 2.0 \implies s_2 = 8.0$, update $= - (1.0 / \sqrt{8}) 2.0 = -0.7071$.
Step 3: $g = 2.0 \implies s_3 = 12.0$, update $= - (1.0 / \sqrt{12}) 2.0 = -0.5774$.

---

## 3. Verify it in code

```python
import numpy as np
s = 0.0
eta = 1.0
g = 2.0
updates = []
for _ in range(3):
    s += g**2
    step = (eta / np.sqrt(s)) * g
    updates.append(step)

assert np.isclose(updates[0], 1.0)
assert np.isclose(updates[1], 2.0 / np.sqrt(8.0))
assert np.isclose(updates[2], 2.0 / np.sqrt(12.0))
assert updates[0] > updates[1] > updates[2]
```

---

## 4. The mistake people actually make
Using AdaGrad to train deep neural networks over many epochs without noticing that gradient updates have frozen due to infinite denominator accumulation.

---

## Check yourself
1. Why does AdaGrad perform well for sparse data (e.g. word embeddings)?
2. What is AdaGrad's fatal flaw in deep learning?

<details>
<summary>Answers</summary>

1. Infrequent features accumulate small squared gradients, preserving large learning rates for rare words.
2. The sum of squared gradients grows monotonically, driving effective learning rate to zero.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [36_RMSProp.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\36_RMSProp.md)
