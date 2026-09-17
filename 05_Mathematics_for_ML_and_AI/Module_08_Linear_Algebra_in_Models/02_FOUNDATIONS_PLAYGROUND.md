# 🐣 Interactive Foundations Playground: Linear Algebra in Models

> *"A neural network layer is a linear transformation followed by a non-linear activation bent in high dimensions."*

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

## 1. Dense Layer Affine Map y = W*x + b

Weights $W$ rotate and scale input features; bias $b$ shifts the origin.

```python
W = [[0.5, -0.2],
     [0.8,  0.4]]
b = [0.1, -0.05]
x = [1.0, 2.0]

y = [sum(W[r][c] * x[c] for c in range(2)) + b[r] for r in range(2)]
assert abs(y[0] - (0.5 * 1.0 - 0.2 * 2.0 + 0.1)) < 1e-6
assert abs(y[0] - 0.2) < 1e-6
assert abs(y[1] - 1.55) < 1e-6
print(f"Affine transformation output: y={y}")
```

---

## 2. Cosine Similarity for Embedding Comparison

Cosine similarity measures the cosine of the angle between two semantic embeddings: $\frac{u \cdot v}{\|u\| \|v\|}$.

```python
emb1 = [1.0, 2.0, 0.0]
emb2 = [2.0, 4.0, 0.0]  # Parallel direction

dot = sum(a * b for a, b in zip(emb1, emb2))
norm1 = math.sqrt(sum(a**2 for a in emb1))
norm2 = math.sqrt(sum(a**2 for a in emb2))
cos_sim = dot / (norm1 * norm2)

assert abs(cos_sim - 1.0) < 1e-6, "Parallel vectors have cosine similarity 1.0"
print(f"Cosine similarity between parallel embeddings: {cos_sim:.4f}")
```

---

## 3. Softmax Normalization Invariant

Softmax exponentiates logits and divides by their sum, guaranteeing non-negative probabilities that strictly sum to 1.0.

```python
logits = [2.0, 1.0, 0.1]
exp_vals = [math.exp(z) for z in logits]
sum_exp = sum(exp_vals)
probs = [ev / sum_exp for ev in exp_vals]

assert abs(sum(probs) - 1.0) < 1e-6, "Probabilities must sum to 1.0"
assert all(p >= 0.0 for p in probs)
assert probs[0] > probs[1] > probs[2]
print(f"Logits {logits} -> Softmax probabilities: {[round(p, 4) for p in probs]}")
```

---
