# 🐣 Interactive Foundations Playground: Tiled Matrix Multiplication (GEMM)

> *"Tiling chops a massive matrix multiply into bite-sized tiles that fit entirely inside high-speed SRAM."*

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

## 1. Naive O(N^3) Matrix Multiplication

Computing $C = A \times B$ takes $2N^3$ floating-point operations.

```python
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
C = [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

assert C[0][0] == 1*5 + 2*7  # 19
assert C[0][1] == 1*6 + 2*8  # 22
assert C[1][0] == 3*5 + 4*7  # 43
assert C[1][1] == 3*6 + 4*8  # 50
print(f"GEMM result matrix C: {C}")
```

---

## 2. Arithmetic Intensity and Operational FLOP/Byte

Arithmetic intensity is $\frac{\text{FLOPs}}{\text{Bytes transferred}}$. High intensity makes kernels compute-bound.

```python
N = 1024
flops = 2 * (N**3)
bytes_transferred = 3 * (N**2) * 4  # 3 matrices of float32
intensity = flops / bytes_transferred

assert intensity > 100.0
assert intensity == (2 * N) / (3 * 4)
print(f"Arithmetic intensity for {N}x{N} GEMM: {intensity:.2f} FLOP/byte")
```

---

## 3. Tiled Shared Memory Reuse Factor

With tile size $B$, each element loaded from DRAM is reused $B$ times in shared memory, reducing DRAM bandwidth pressure by $B$.

```python
tile_size = 16
dram_traffic_naive = 2 * (N**3) * 4
dram_traffic_tiled = dram_traffic_naive / tile_size

assert dram_traffic_tiled < dram_traffic_naive
assert dram_traffic_naive / dram_traffic_tiled == 16
print(f"DRAM bandwidth reduction factor with tile size {tile_size}: {tile_size}x")
```

---
