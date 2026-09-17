# 🐣 Interactive Foundations Playground: GPU Microarchitecture and Execution Model

> *"A CPU is an agile sports car with a few fast cylinders; a GPU is a massive freight train with thousands of parallel wheels."*

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

## 1. Warp Execution Dimension (32 Threads)

GPUs group threads into warps of 32 threads that execute instructions in strict SIMT (Single Instruction, Multiple Threads) lockstep.

```python
threads_per_warp = 32
total_threads = 1024
num_warps = total_threads // threads_per_warp

assert num_warps == 32
assert total_threads % threads_per_warp == 0
print(f"Total threads: {total_threads} partitioned into {num_warps} SIMT warps.")
```

---

## 2. Global Linear Thread Indexing

Mapping 1D grid and block dimensions into a unique global thread ID: $\text{tid} = \text{blockIdx.x} \cdot \text{blockDim.x} + \text{threadIdx.x}$.

```python
def get_global_tid(block_idx, thread_idx, block_dim):
    return block_idx * block_dim + thread_idx

tid_0_0 = get_global_tid(0, 0, 256)
tid_1_5 = get_global_tid(1, 5, 256)
assert tid_0_0 == 0
assert tid_1_5 == 261
assert get_global_tid(3, 255, 256) == 1023
print(f"Global thread IDs: block 0 thread 0 -> {tid_0_0}, block 1 thread 5 -> {tid_1_5}")
```

---

## 3. Grid Boundary Guard (Bounds Check)

Since grid size is rounded up to a multiple of block dimension, threads beyond array length $N$ must be safely deactivated.

```python
N = 1000
block_dim = 256
grid_dim = math.ceil(N / block_dim)  # 4 blocks -> 1024 threads

active_count = 0
for b in range(grid_dim):
    for t in range(block_dim):
        tid = b * block_dim + t
        if tid < N:
            active_count += 1

assert grid_dim == 4
assert active_count == 1000
assert (grid_dim * block_dim) == 1024
print(f"Boundary check passed: exactly {active_count} of {grid_dim * block_dim} threads activated.")
```

---
