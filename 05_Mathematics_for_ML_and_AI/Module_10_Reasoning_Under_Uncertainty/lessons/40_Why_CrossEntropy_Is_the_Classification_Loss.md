# Lesson 10.40 — Why Cross-Entropy Is the Classification Loss

> **Module 10:** Reasoning Under Uncertainty · Lesson 40 of 41

---

## What you will be able to do after this lesson

- [ ] Prove minimizing cross-entropy is mathematically identical to maximum likelihood estimation under a Categorical model.
- [ ] Contrast cross-entropy with mean squared error for classification.

## Prerequisites

- 10.39 Cross-Entropy and 12.08 Log-Likelihood.

---

## 1. The idea

In classification, the true label is a one-hot distribution $\mathbf{y}$ ($y_k = 1$ for true class $k$), and the model outputs predicted probabilities $\hat{\mathbf{y}} = \text{softmax}(\mathbf{z})$.
The cross-entropy loss is:
$$\mathcal{L} = -\sum_{k} y_k \log \hat{y}_k = -\log \hat{y}_{\text{true}}$$
This is **identical to the negative log-likelihood of the data under a Categorical distribution**. Unlike MSE, its gradient $\nabla_{\mathbf{z}} \mathcal{L} = \hat{\mathbf{y}} - \mathbf{y}$ does not saturate when predictions are wrong, guaranteeing steep gradients and fast training.

---

## 2. Worked example

True class $k=0$, model predicts $\hat{y}_0 = 0.9$. Loss $= -\log(0.9) \approx 0.105$. If model is wrong ($\hat{y}_0 = 0.1$), loss $= -\log(0.1) \approx 2.302$.

---

## 3. Verify it in code

```python
import numpy as np
y_true = np.array([1.0, 0.0, 0.0])
y_pred_good = np.array([0.9, 0.05, 0.05])
y_pred_bad = np.array([0.1, 0.45, 0.45])

loss_good = -np.log(y_pred_good[0])
loss_bad = -np.log(y_pred_bad[0])

assert loss_good < loss_bad
assert np.isclose(loss_good, -np.log(0.9))
```

---

## 4. The mistake people actually make

Using Mean Squared Error (MSE) loss for classification with softmax/sigmoid outputs, which causes vanishing gradients on confident errors.

---

## Check yourself

1. Why is cross-entropy preferred over MSE for neural network classification?
2. What is the cross-entropy loss for a single one-hot training example?

<details>
<summary>Answers</summary>

1. Its gradient is linear in prediction error (y_hat - y), avoiding vanishing gradient plateaus.
2. -log(y_hat_true).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](41_Module_Project_Naive_Bayes_With_Calibrated_Probabilities.md)
