# 🐣 Interactive Foundations Playground: FlashAttention-1 & 2 Internals

> *"FlashAttention tiles attention into small SRAM blocks, computing softmax on-the-fly without saving the N x N attention matrix."*

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

## 1. Quadratic N^2 Attention Memory Bottleneck

Standard attention materializes $S = Q K^T \in \mathbb{R}^{N \times N}$, which exhausts GPU HBM memory on long sequences.

```python
seq_len = 4096
bytes_per_elem = 2  # FP16
attn_matrix_mb = (seq_len**2 * bytes_per_elem) / (1024 * 1024)

assert attn_matrix_mb == 32.0  # 32 MB per head
assert seq_len**2 == 16_777_216
print(f"Attention matrix size for N={seq_len}: {attn_matrix_mb} MB per attention head.")
```

---

## 2. Online Softmax Rescaling Invariant

Online softmax updates running maximum $m$ and normalization sum $d$ chunk-by-chunk without storing the entire sequence.

```python
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
```

---

## 3. FlashAttention IO Complexity O(N^2 d^2 / M)

By tiling Q, K, V into SRAM of size $M$, FlashAttention cuts HBM read/writes from $O(N^2)$ down to $O(N^2 / M)$.

```python
N, d, M = 4096, 64, 100_000
naive_hbm_io = N**2
flash_hbm_io = (N**2 * d) / M

assert flash_hbm_io < naive_hbm_io
assert flash_hbm_io > 0
print(f"HBM memory IO reduced from {naive_hbm_io:,} down to {int(flash_hbm_io):,} units.")
```

---
