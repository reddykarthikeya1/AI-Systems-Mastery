# 🐣 Interactive Foundations Playground: Transformers & Self-Attention

> *"Self-attention lets every word in a sentence look at every other word and decide how much to pay attention."*

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

## 1. Scaled Dot-Product Attention Scores

Query-Key dot product divided by $\sqrt{d_k}$ measures token relevance while preventing gradient vanishing in softmax.

```python
q = [1.0, 0.0]
k1 = [1.0, 0.0]  # Identical direction
k2 = [0.0, 1.0]  # Orthogonal direction
d_k = 2.0
scale = math.sqrt(d_k)

score1 = sum(a * b for a, b in zip(q, k1)) / scale
score2 = sum(a * b for a, b in zip(q, k2)) / scale

assert score1 > score2
assert abs(score1 - 1.0 / math.sqrt(2.0)) < 1e-6
assert score2 == 0.0
print(f"Attention scores: match={score1:.4f}, orthogonal={score2:.4f}")
```

---

## 2. Attention Weights via Softmax

Softmax converts raw attention logits into normalized attention weights that sum to 1.0.

```python
scores = [score1, score2]
exp_s = [math.exp(s) for s in scores]
weights = [e / sum(exp_s) for e in exp_s]

assert abs(sum(weights) - 1.0) < 1e-6
assert weights[0] > weights[1]
print(f"Attention weights distribution: {[round(w, 4) for w in weights]}")
```

---

## 3. Weighted Value Context Aggregation

The final contextual token representation is the weighted sum of all Value vectors: $\sum w_i V_i$.

```python
v1 = [10.0, 20.0]
v2 = [1.0, 2.0]

context = [weights[0] * v1[i] + weights[1] * v2[i] for i in range(2)]
assert len(context) == 2
assert context[0] > 1.0
print(f"Aggregated context embedding: {[round(c, 2) for c in context]}")
```

---
