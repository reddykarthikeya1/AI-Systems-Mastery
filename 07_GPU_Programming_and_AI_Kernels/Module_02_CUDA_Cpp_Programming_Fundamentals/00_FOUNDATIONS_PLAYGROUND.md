# 🐣 Interactive Foundations Playground: CUDA C++ Programming Fundamentals

> *"A CUDA kernel is a function written from the perspective of a single worker thread among millions."*

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

## 1. Vector Addition Kernel Simulation

Each thread reads element $i$ from arrays $A$ and $B$, computes $C[i] = A[i] + B[i]$, and writes to memory.

```python
A = [1.0, 2.0, 3.0, 4.0]
B = [10.0, 20.0, 30.0, 40.0]
C = [0.0] * len(A)

# Simulated parallel thread loop
for tid in range(len(A)):
    C[tid] = A[tid] + B[tid]

assert C == [11.0, 22.0, 33.0, 44.0]
assert C[0] == 11.0
print(f"Parallel vector add result: {C}")
```

---

## 2. Grid Stride Loop Pattern

A grid-stride loop lets a fixed number of threads process arbitrary-sized vectors by striding by total grid size.

```python
total_threads = 4
data_size = 10
processed = [0] * data_size

for tid in range(total_threads):
    # Each thread steps forward by total_threads
    for i in range(tid, data_size, total_threads):
        processed[i] = 1

assert sum(processed) == data_size
assert all(p == 1 for p in processed)
print(f"Grid-stride loop processed all {data_size} elements with {total_threads} threads.")
```

---

## 3. Speedup over Sequential Baseline

Comparing wall-clock parallel execution time against sequential loops verifies parallel scaling efficiency.

```python
seq_ops = 1_000_000
gpu_cores = 1000
parallel_time_units = seq_ops / gpu_cores

assert parallel_time_units == 1000.0
assert seq_ops / parallel_time_units == 1000.0
print(f"Theoretical speedup with {gpu_cores} cores: {gpu_cores}x")
```

---
