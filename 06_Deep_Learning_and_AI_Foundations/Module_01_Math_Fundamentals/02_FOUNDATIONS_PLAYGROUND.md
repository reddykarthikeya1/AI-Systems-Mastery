# 🐣 Interactive Foundations Playground: Math Fundamentals for Deep Learning

> *"Deep learning is fundamentally vector calculus and linear algebra accelerated by GPUs."*

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

## 1. Vector Dot Product in Neurons

An artificial neuron takes the dot product between an input feature vector and its learned weight vector.

```python
inputs = [0.5, 0.8, -0.2]
weights = [0.4, 0.7, 0.9]
bias = 0.1

activation = sum(x * w for x, w in zip(inputs, weights)) + bias
assert abs(activation - (0.2 + 0.56 - 0.18 + 0.1)) < 1e-6
assert activation > 0
print(f"Neuron pre-activation: {activation:.4f}")
```

---

## 2. Sigmoid and ReLU Activation Functions

ReLU $\max(0, x)$ prevents vanishing gradients for positive inputs, while Sigmoid $\frac{1}{1 + e^{-x}}$ squashes real values into probabilities $(0, 1)$.

```python
def relu(x): return max(0.0, x)
def sigmoid(x): return 1.0 / (1.0 + math.exp(-x))

assert relu(3.5) == 3.5
assert relu(-2.0) == 0.0
assert abs(sigmoid(0.0) - 0.5) < 1e-6
print(f"ReLU(3.5)={relu(3.5)}, ReLU(-2.0)={relu(-2.0)}, Sigmoid(0)={sigmoid(0.0)}")
```

---

## 3. Mean Squared Error (MSE) Loss

MSE computes the average squared discrepancy between predicted targets and true ground truth labels.

```python
y_true = [1.0, 2.0, 3.0]
y_pred = [1.2, 1.8, 3.1]

mse = sum((yt - yp)**2 for yt, yp in zip(y_true, y_pred)) / len(y_true)
assert abs(mse - (0.04 + 0.04 + 0.01) / 3) < 1e-6
assert mse > 0
print(f"Mean Squared Error loss: {mse:.4f}")
```

---
