"""Beginner playground for Module 10 - Quantization Kernels in Triton.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Packing INT8 into UINT32 Registers
q0, q1, q2, q3 = 10, 20, 30, 40
packed = (q3 << 24) | (q2 << 16) | (q1 << 8) | q0

u0 = packed & 0xFF
u1 = (packed >> 8) & 0xFF
u2 = (packed >> 16) & 0xFF
u3 = (packed >> 24) & 0xFF

assert (u0, u1, u2, u3) == (10, 20, 30, 40)
assert packed > 0
print(f"Packed 4 int8 values into uint32: {hex(packed)} -> unpacked: {(u0, u1, u2, u3)}")

# -------------------------------------------- 2. Block-Wise Quantization Scaling
block = [0.1, -0.4, 0.9, -1.2]
scale = max(abs(x) for x in block) / 127.0

quantized = [int(round(x / scale)) for x in block]
assert max(abs(q) for q in quantized) == 127
assert abs(scale - 1.2 / 127.0) < 1e-6
print(f"Block scale: {scale:.5f}, Quantized codes: {quantized}")

# -------------------------------------------- 3. Fused Dequantize-GEMV in Triton
int8_w = [10, -20, 30]
scale = 0.05
act = [1.0, 2.0, 3.0]

dot_res = sum((w * scale) * a for w, a in zip(int8_w, act))
expected = (10 * 0.05 * 1.0) + (-20 * 0.05 * 2.0) + (30 * 0.05 * 3.0)

assert abs(dot_res - expected) < 1e-6
assert abs(dot_res - 3.0) < 1e-6
print(f"Fused Dequantize-GEMV dot product result: {dot_res}")

print()
print("All checks passed.")
