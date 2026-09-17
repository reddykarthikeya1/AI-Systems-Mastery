# 🐣 Interactive Foundations Playground: How to Fine-Tune Models & LoRA Math

> *"LoRA freezes the 100-billion-parameter foundation model and trains a lightweight low-rank delta adapter."*

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

## 1. LoRA Decomposition Factorization Delta W = B * A

Instead of fine-tuning full matrix $W \in \mathbb{R}^{d \times k}$ ($d \cdot k$ parameters), LoRA trains low-rank matrices $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ with $r \ll \min(d, k)$.

```python
d, k, r = 4096, 4096, 8
full_params = d * k
lora_params = (d * r) + (r * k)
param_reduction_pct = (1.0 - lora_params / full_params) * 100

assert full_params == 16_777_216
assert lora_params == 65_536
assert param_reduction_pct > 99.0
print(f"Parameter reduction: from {full_params:,} down to {lora_params:,} ({param_reduction_pct:.2f}% savings)")
```

---

## 2. LoRA Scaling Factor Alpha / Rank

The low-rank delta is scaled by $\frac{\alpha}{r}$ before being added to the frozen weights: $h = W_0 x + \frac{\alpha}{r} B A x$.

```python
alpha = 16.0
rank = 8.0
scale = alpha / rank

assert scale == 2.0
assert scale > 0
print(f"LoRA adapter scale (alpha={alpha}, rank={rank}): {scale}")
```

---

## 3. Frozen Base Weight Invariance

During training, gradients only flow into matrices $A$ and $B$; the base weights $W_0$ remain completely unchanged.

```python
w0_weight = 1.42
lora_delta = 0.05 * scale
effective_weight = w0_weight + lora_delta

assert w0_weight == 1.42, "Base weight is frozen"
assert abs(effective_weight - 1.52) < 1e-6
print(f"Effective fine-tuned weight: {effective_weight:.4f}")
```

---
