# 🐣 Interactive Foundations Playground: Neural Network from Scratch

> *"A multi-layer perceptron is a stacked pipeline of linear matrix multiplies and non-linear activations."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. 2-Layer Forward Propagation

Input $x$ passes through hidden layer with activation to produce intermediate representations, then through the output layer.

```python
x = [1.0, -1.0]
W1 = [[0.5, 0.2], [-0.3, 0.8]]
b1 = [0.1, -0.1]

# Layer 1 pre-activation and ReLU
h_pre = [sum(W1[r][c] * x[c] for c in range(2)) + b1[r] for r in range(2)]
h_act = [max(0.0, val) for val in h_pre]

assert abs(h_pre[0] - (0.5 * 1.0 + 0.2 * (-1.0) + 0.1)) < 1e-6
assert abs(h_pre[0] - 0.4) < 1e-6
assert h_act[0] == 0.4
print(f"Hidden layer activations: {h_act}")
```

---

## 2. Binary Cross-Entropy Loss

BCE penalizes confident wrong classifications asymptotically: $-\sum [y \log(\hat{y}) + (1-y) \log(1 - \hat{y})]$.

```python
def bce(y_true, y_prob):
    eps = 1e-15
    y_prob = max(eps, min(1.0 - eps, y_prob))
    return -(y_true * math.log(y_prob) + (1.0 - y_true) * math.log(1.0 - y_prob))

loss_correct = bce(1.0, 0.99)
loss_wrong = bce(1.0, 0.01)

assert loss_wrong > loss_correct
assert loss_correct < 0.02
print(f"BCE Loss confident correct: {loss_correct:.4f}, confident wrong: {loss_wrong:.4f}")
```

---

## 3. Weight Update with Momentum

Momentum accumulates past velocity to smooth out noisy gradients: $v_{t} = \beta v_{t-1} + \nabla L$, $w = w - \eta v_t$.

```python
velocity = 0.0
beta = 0.9
grad = 2.0
lr = 0.1

velocity = beta * velocity + grad
w_updated = 1.0 - lr * velocity

assert velocity == 2.0
assert abs(w_updated - 0.8) < 1e-6
print(f"Updated weight with momentum: {w_updated}")
```

---
