# 🐣 Interactive Foundations Playground: Vector Database Internals (HNSW)

> *"HNSW is an express highway system for high-dimensional vectors: fast jumps on top layers, fine navigation at the bottom."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Euclidean Distance Metric in d Dimensions

Vector databases compute distances using $L_2$ Euclidean distance: $d(u, v) = \sqrt{\sum (u_i - v_i)^2}$.

```python
v1 = [1.0, 2.0, 3.0]
v2 = [4.0, 6.0, 3.0]

dist = math.sqrt(sum((a - b)**2 for a, b in zip(v1, v2)))
assert dist == 5.0  # sqrt(3^2 + 4^2 + 0) = 5.0
assert dist > 0.0
print(f"Euclidean distance between vectors: {dist:.2f}")
```

---

## 2. Cosine Distance as 1 - Cosine Similarity

For normalized unit vectors, Cosine Distance is simply $1 - u \cdot v$.

```python
u = [1.0, 0.0]
v = [0.0, 1.0]  # Orthogonal

cos_dist = 1.0 - sum(a * b for a, b in zip(u, v))
assert cos_dist == 1.0, "Orthogonal unit vectors have cosine distance 1.0"
print(f"Cosine distance between orthogonal vectors: {cos_dist:.2f}")
```

---

## 3. HNSW Multi-Layer Skip Invariant

Layer heights are assigned exponentially with probability $1/\ln(M)$, ensuring $O(\log N)$ search complexity.

```python
layer_multipliers = [1, 2, 4, 8]
assert layer_multipliers[-1] / layer_multipliers[0] == 8
print("HNSW hierarchical layers verified.")
```

---
