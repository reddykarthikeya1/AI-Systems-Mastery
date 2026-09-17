"""Beginner playground for Module 08 - FlashAttention-1 & 2 Internals.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Quadratic N^2 Attention Memory Bottleneck
seq_len = 4096
bytes_per_elem = 2  # FP16
attn_matrix_mb = (seq_len**2 * bytes_per_elem) / (1024 * 1024)

assert attn_matrix_mb == 32.0  # 32 MB per head
assert seq_len**2 == 16_777_216
print(f"Attention matrix size for N={seq_len}: {attn_matrix_mb} MB per attention head.")

# -------------------------------------------- 2. Online Softmax Rescaling Invariant
chunk1 = [1.0, 2.0]
chunk2 = [3.0, 1.0]

m1 = max(chunk1)  # 2.0
d1 = sum(math.exp(x - m1) for x in chunk1)

m2 = max(m1, max(chunk2))  # 3.0
d2 = d1 * math.exp(m1 - m2) + sum(math.exp(x - m2) for x in chunk2)

full = chunk1 + chunk2
m_true = max(full)
d_true = sum(math.exp(x - m_true) for x in full)

assert m2 == m_true
assert abs(d2 - d_true) < 1e-6
print(f"Online softmax normalization matches global sum: {d2:.4f} == {d_true:.4f}")

# -------------------------------------------- 3. FlashAttention IO Complexity O(N^2 d^2 / M)
N, d, M = 4096, 64, 100_000
naive_hbm_io = N**2
flash_hbm_io = (N**2 * d) / M

assert flash_hbm_io < naive_hbm_io
assert flash_hbm_io > 0
print(f"HBM memory IO reduced from {naive_hbm_io:,} down to {int(flash_hbm_io):,} units.")

print()
print("All checks passed.")
