# Lesson 09.37: Adam and Its Bias Correction

## Learning Objectives
- Combine momentum (1st moment) and RMSProp (2nd moment) into Adam.
- Derive the initialization bias correction factors: hat{m} = m / (1 - beta_1^t) and hat{v} = v / (1 - beta_2^t).

## Prerequisites
- 09.36 RMSProp.

---

## 1. The Core Idea
**Adam** (Kingma & Ba) tracks both the first moment (mean) and second raw moment (uncentered variance):
$$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$
Because $m_0 = v_0 = 0$, both are severely biased toward zero at early iterations. Dividing by $1 - \beta^t$ restores unbiased estimates:
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}, \quad \theta_t = \theta_{t-1} - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

---

## 2. Mathematical Exposition & Worked Example
$\beta_1 = 0.9, \beta_2 = 0.999$. At $t = 1$: $m_1 = 0.1 g_1$.
Uncorrected update would be shrunken by $10\times$.
With correction: $\hat{m}_1 = \frac{0.1 g_1}{1 - 0.9^1} = \frac{0.1 g_1}{0.1} = g_1$!
For $v$: $v_1 = 0.001 g_1^2 \implies \hat{v}_1 = \frac{0.001 g_1^2}{1 - 0.999^1} = g_1^2$!

---

## 3. Verify it in code

```python
import numpy as np
b1, b2 = 0.9, 0.999
g = 3.0
m1 = (1.0 - b1) * g
v1 = (1.0 - b2) * (g**2)

m_hat = m1 / (1.0 - b1**1)
v_hat = v1 / (1.0 - b2**1)

assert np.isclose(m_hat, g)
assert np.isclose(v_hat, g**2)
```

---

## 4. The mistake people actually make
Omitting bias correction in custom implementations, causing tiny paralyzed steps during initial training steps.

---

## Check yourself
1. Why is bias correction needed in Adam?
2. What happens to the bias correction factors as iteration count t -> inf?

<details>
<summary>Answers</summary>

1. Because moments are initialized to zero, causing estimates to underestimate true scales early on.
2. 1 - beta^t -> 1, so the correction naturally phases out.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [38_Why_Adam_Sometimes_Fails_to_Converge.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\38_Why_Adam_Sometimes_Fails_to_Converge.md)
