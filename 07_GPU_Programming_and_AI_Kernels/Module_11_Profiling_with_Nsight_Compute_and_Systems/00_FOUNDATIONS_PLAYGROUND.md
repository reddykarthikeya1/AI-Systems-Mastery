# 🐣 Interactive Foundations Playground: Profiling with Nsight Compute & Roofline

> *"The Roofline model tells you whether your code is starved for compute or waiting on memory bandwidth."*

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

## 1. Roofline Ridge Point Calculation

The ridge point $\text{Ridge} = \frac{\text{Peak TFLOP/s}}{\text{Peak Memory BW (TB/s)}}$ marks the threshold between memory-bound and compute-bound regimes.

```python
peak_tflops = 312.0   # Tensor core dense FP16 TFLOP/s
peak_bw_tbs = 2.0     # HBM bandwidth in TB/s
ridge_intensity = peak_tflops / peak_bw_tbs  # FLOP/byte

assert ridge_intensity == 156.0
print(f"Hardware Ridge Point: {ridge_intensity:.1f} FLOP/byte.")
```

---

## 2. Kernel Regime Classification

Kernels with intensity below ridge are memory-bandwidth bound; kernels above are compute bound.

```python
kernel1_intensity = 40.0   # Softmax / LayerNorm
kernel2_intensity = 200.0  # Large GEMM

regime1 = "Memory Bound" if kernel1_intensity < ridge_intensity else "Compute Bound"
regime2 = "Memory Bound" if kernel2_intensity < ridge_intensity else "Compute Bound"

assert regime1 == "Memory Bound"
assert regime2 == "Compute Bound"
print(f"Kernel 1: {regime1}, Kernel 2: {regime2}")
```

---

## 3. Memory Bandwidth Utilization (MBU)

MBU computes achieved DRAM throughput as a percentage of maximum theoretical bus bandwidth.

```python
achieved_gb_s = 1700.0
peak_gb_s = 2000.0
mbu_pct = (achieved_gb_s / peak_gb_s) * 100.0

assert mbu_pct == 85.0
assert mbu_pct > 80.0, "High memory bus saturation achieved"
print(f"Achieved Memory Bandwidth Utilization: {mbu_pct:.1f}%")
```

---
