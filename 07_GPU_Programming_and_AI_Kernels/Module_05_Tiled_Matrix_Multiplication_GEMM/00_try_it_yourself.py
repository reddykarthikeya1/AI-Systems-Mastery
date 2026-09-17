"""Beginner playground for Module 05 - Tiled Matrix Multiplication (GEMM).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Naive O(N^3) Matrix Multiplication
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
C = [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

assert C[0][0] == 1*5 + 2*7  # 19
assert C[0][1] == 1*6 + 2*8  # 22
assert C[1][0] == 3*5 + 4*7  # 43
assert C[1][1] == 3*6 + 4*8  # 50
print(f"GEMM result matrix C: {C}")

# -------------------------------------------- 2. Arithmetic Intensity and Operational FLOP/Byte
N = 1024
flops = 2 * (N**3)
bytes_transferred = 3 * (N**2) * 4  # 3 matrices of float32
intensity = flops / bytes_transferred

assert intensity > 100.0
assert intensity == (2 * N) / (3 * 4)
print(f"Arithmetic intensity for {N}x{N} GEMM: {intensity:.2f} FLOP/byte")

# -------------------------------------------- 3. Tiled Shared Memory Reuse Factor
tile_size = 16
dram_traffic_naive = 2 * (N**3) * 4
dram_traffic_tiled = dram_traffic_naive / tile_size

assert dram_traffic_tiled < dram_traffic_naive
assert dram_traffic_naive / dram_traffic_tiled == 16
print(f"DRAM bandwidth reduction factor with tile size {tile_size}: {tile_size}x")

print()
print("All checks passed.")
