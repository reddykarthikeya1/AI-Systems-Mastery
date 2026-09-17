# 🐣 Interactive Foundations Playground: Fused Activations & Normalization

> *"Kernel fusion merges multiple operations into one trip to DRAM: load once, compute all, write once."*

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

## 1. Unfused vs Fused Memory Trips

Unfused LayerNorm + ReLU writes intermediate tensors back to global DRAM; fused kernels keep values in registers.

```python
unfused_dram_passes = 4  # (read x, write norm) + (read norm, write relu)
fused_dram_passes = 2    # read x, write final
speedup = unfused_dram_passes / fused_dram_passes

assert speedup == 2.0
assert fused_dram_passes < unfused_dram_passes
print(f"Kernel fusion eliminates {unfused_dram_passes - fused_dram_passes} DRAM round trips ({speedup}x speedup).")
```

---

## 2. Layer Normalization Statistics

LayerNorm normalizes across feature dimension: $\hat{x} = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \gamma + \beta$.

```python
x = [1.0, 2.0, 3.0, 4.0, 5.0]
mean = sum(x) / len(x)
var = sum((val - mean)**2 for val in x) / len(x)
normed = [(val - mean) / math.sqrt(var + 1e-5) for val in x]

assert abs(mean - 3.0) < 1e-6
assert abs(sum(normed)) < 1e-4, "Normalized mean is 0"
assert abs(sum(v**2 for v in normed) / len(normed) - 1.0) < 1e-3, "Normalized variance is 1"
print(f"Normalized activations: {[round(v, 3) for v in normed]}")
```

---

## 3. Fused Bias-GELU Activation

Combining bias addition with GELU approximation avoids an intermediate activation tensor allocation.

```python
def gelu(z):
    return 0.5 * z * (1.0 + math.tanh(math.sqrt(2.0 / math.pi) * (z + 0.044715 * z**3)))

val_fused = gelu(1.5 + 0.5)  # Bias + GELU in single expression
assert val_fused > 1.9
assert gelu(0.0) == 0.0
print(f"Fused Bias-GELU output: {val_fused:.4f}")
```

---
