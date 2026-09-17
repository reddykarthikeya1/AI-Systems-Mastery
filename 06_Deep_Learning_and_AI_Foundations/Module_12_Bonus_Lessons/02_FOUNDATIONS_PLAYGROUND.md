# 🐣 Interactive Foundations Playground: Bonus Lessons: Quantization & Pruning

> *"Quantization is rounding numbers to fit into smaller memory boxes without losing the big picture."*

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

## 1. FP32 to INT8 Symmetric Quantization

Quantization maps 32-bit floating point values into 8-bit integers $[-128, 127]$ using a scale factor $S = \frac{\max(|X|)}{127}$.

```python
weights = [-2.5, 0.0, 1.25, 2.5]
max_abs = max(abs(w) for w in weights)
scale = max_abs / 127.0

int8_weights = [int(round(w / scale)) for w in weights]
assert int8_weights[0] == -127
assert int8_weights[1] == 0
assert int8_weights[-1] == 127
print(f"Quantized INT8 weights: {int8_weights} with scale {scale:.4f}")
```

---

## 2. INT8 Dequantization Reconstruction

Dequantization reconstructs the floating point values by multiplying integer codes by scale: $\hat{X} = q \cdot S$.

```python
reconstructed = [q * scale for q in int8_weights]
for orig, recon in zip(weights, reconstructed):
    assert abs(orig - recon) < 0.02

assert abs(reconstructed[2] - 1.25) < 0.02
print(f"Dequantized weights match original: {reconstructed}")
```

---

## 3. Magnitude-Based Weight Pruning

Zeroing out weights whose absolute value falls below threshold $\tau$ induces sparsity, reducing memory and computation.

```python
layer_w = [0.02, -0.85, 0.01, 0.45, -0.005]
threshold = 0.05
pruned = [0.0 if abs(w) < threshold else w for w in layer_w]

assert pruned == [0.0, -0.85, 0.0, 0.45, 0.0]
sparsity = pruned.count(0.0) / len(pruned)
assert sparsity == 0.60
print(f"Pruned layer: {pruned}, Sparsity: {sparsity:.1%}")
```

---
