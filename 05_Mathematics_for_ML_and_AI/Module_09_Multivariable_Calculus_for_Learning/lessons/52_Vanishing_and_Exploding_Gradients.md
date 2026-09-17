# Lesson 09.52: Vanishing and Exploding Gradients

## Learning Objectives
- Analyze backpropagation through L layers as repeated Jacobian multiplication.
- Relate vanishing/exploding gradients to the spectral radius of layer weight matrices.

## Prerequisites
- 09.15 The Multivariable Chain Rule.

---

## 1. The Core Idea
In an $L$-layer network, gradient flow to input $\mathbf{x}_0$ is a product of Jacobians:
$$\frac{\partial L}{\partial \mathbf{x}_0} = \frac{\partial L}{\partial \mathbf{x}_L} \prod_{l=1}^L \mathbf{J}_l$$
If the largest singular value $\sigma_{\max}(\mathbf{J}_l) < 1$, gradients decay exponentially to zero ($\sigma^L \to 0$, **vanishing gradients**). If $\sigma_{\max}(\mathbf{J}_l) > 1$, gradients explode exponentially ($\sigma^L \to \infty$, **exploding gradients**).

---

## 2. Mathematical Exposition & Worked Example
In a 50-layer network:
If $\sigma = 0.9$: $0.9^{50} \approx 0.00515$ ($99.5\%$ attenuation).
If $\sigma = 1.1$: $1.1^{50} \approx 117.39$ ($117\times$ amplification).

---

## 3. Verify it in code

```python
import numpy as np
L = 50
decay = 0.9**L
explosion = 1.1**L

assert np.isclose(decay, 0.005153775)
assert np.isclose(explosion, 117.39085)
```

---

## 4. The mistake people actually make
Using saturating activations like sigmoid or tanh across hundreds of unnormalized layers without residual connections.

---

## Check yourself
1. What causes gradients to vanish across deep networks?
2. How do residual connections (ResNets) mitigate vanishing gradients?

<details>
<summary>Answers</summary>

1. Repeated multiplication by layer Jacobians with singular values strictly less than 1.
2. The skip connection x_{l+1} = x_l + F(x_l) creates an additive identity path J = I + nabla F, ensuring gradients flow unimpeded.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [53_Gradient_Clipping.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\53_Gradient_Clipping.md)
