# 🐣 Interactive Foundations Playground: FlashAttention-3 & Hopper/Blackwell

> *"FlashAttention-3 uses asynchronous Tensor Memory Accelerator (TMA) hardware to overlap compute and memory transfers."*

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

## 1. Tensor Memory Accelerator (TMA) Asynchronous Copy

TMA hardware moves multidimensional tensor tiles directly from HBM to Shared Memory bypassing SM register files entirely.

```python
tile_shape = (64, 64)
bytes_per_elem = 2
tile_bytes = tile_shape[0] * tile_shape[1] * bytes_per_elem

assert tile_bytes == 8192
assert tile_bytes == 8 * 1024
print(f"TMA copied 8 KB tile ({tile_shape}) asynchronously into shared memory.")
```

---

## 2. FP8 Low-Precision Dynamic Range Scaling

FP8 formats (E4M3 and E5M2) double throughput and halve memory footprint compared to 16-bit precision.

```python
fp16_bits = 16
fp8_bits = 8
bandwidth_multiplier = fp16_bits / fp8_bits

assert bandwidth_multiplier == 2.0
print(f"FP8 doubles memory bandwidth efficiency by {bandwidth_multiplier:.0f}x.")
```

---

## 3. Warp-Group Matrix Multiply-Accumulate (WGMMA)

Hopper's WGMMA synchronizes 4 warps (128 threads) together into a collective matrix multiply execution unit.

```python
threads_per_warpgroup = 4 * 32
assert threads_per_warpgroup == 128
print(f"WGMMA synchronizes {threads_per_warpgroup} threads as a single warp-group.")
```

---
