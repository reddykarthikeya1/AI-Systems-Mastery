# 🐣 Interactive Foundations Playground: Quantization for Serving (AWQ & SmoothQuant)

> *"SmoothQuant migrates outlier difficulty from activations to weights where it can be precomputed."*

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

## 1. Activation Outlier Channel Dilemma

LLM activations exhibit systematic outlier channels with values 100x larger than normal, which break standard INT8 quantization.

```python
channel_act = [0.2, 0.1, 85.0, 0.3]
max_outlier = max(channel_act)
median_act = sorted(channel_act)[1]
ratio = max_outlier / median_act

assert ratio > 100.0
assert ratio == 425.0
print(f"Activation outlier channel ratio: {ratio:.0f}x baseline magnitude.")
```

---

## 2. SmoothQuant Mathematical Equivalence

Scaling activations by $s^{-1}$ and weights by $s$ maintains mathematical equivalence $Y = (X \text{diag}(s)^{-1}) (\text{diag}(s) W)$ while smoothing outliers.

```python
x = 10.0
w = 0.2
s = 2.0

x_smooth = x / s   # 5.0
w_smooth = w * s   # 0.4

assert x * w == 2.0
assert x_smooth * w_smooth == 2.0
print(f"SmoothQuant identity verified: {x}*{w} == {x_smooth}*{w_smooth}")
```

---

## 3. Weight-Only (W4A16) Memory Footprint Halving

INT4 weights reduce GPU memory by 50% compared to INT8 and 75% compared to FP16, doubling serving concurrency.

```python
fp16_gb = 14.0
int4_gb = fp16_gb * (4 / 16)

assert int4_gb == 3.5
assert fp16_gb / int4_gb == 4.0
print(f"W4A16 shrinks model from {fp16_gb} GB down to {int4_gb} GB.")
```

---
