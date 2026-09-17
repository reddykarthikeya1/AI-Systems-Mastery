# 🐣 Interactive Foundations Playground: OpenAI Triton Fundamentals

> *"Triton lets you write high-performance GPU kernels in Python without wrestling with C++ CUDA boilerplates."*

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

## 1. Block Pointer Offsets and Range Masks

Triton kernels operate over blocks of threads with explicit masking for boundary elements.

```python
block_size = 64
pid = 2
offsets = [pid * block_size + i for i in range(block_size)]
n_elements = 150
mask = [off < n_elements for off in offsets]

assert offsets[0] == 128
assert offsets[-1] == 191
assert sum(mask) == 22, "150 - 128 = 22 elements inside bounds"
print(f"Triton block offsets {offsets[0]}..{offsets[-1]}, valid masked elements: {sum(mask)}")
```

---

## 2. Triton Vectorized Add Kernel Simulation

A Triton block loads a vector tile, executes an element-wise binary operator, and stores results with mask.

```python
x = list(range(10))
y = [x_val * 2 for x_val in x]
output = [0] * len(x)

for i in range(len(x)):
    output[i] = x[i] + y[i]

assert output == [3 * i for i in range(10)]
assert output[-1] == 27
print(f"Triton simulated vector add result: {output}")
```

---

## 3. Triton Autotuning Grid Search

Triton automatically selects the optimal `BLOCK_SIZE` and `num_warps` that maximize kernel throughput on the hardware.

```python
configs = [(32, 2), (64, 4), (128, 8)]
best_config = max(configs, key=lambda c: c[0] * c[1])

assert best_config == (128, 8)
assert best_config[0] == 128
print(f"Selected best autotuned configuration: BLOCK_SIZE={best_config[0]}, WARPS={best_config[1]}")
```

---
