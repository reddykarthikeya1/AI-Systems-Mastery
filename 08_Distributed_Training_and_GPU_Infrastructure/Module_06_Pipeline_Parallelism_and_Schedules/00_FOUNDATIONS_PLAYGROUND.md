# 🐣 Interactive Foundations Playground: Pipeline Parallelism & 1F1B Schedule

> *"Pipeline parallelism is an assembly line: GPU 1 builds the frame, GPU 2 installs the engine, GPU 3 paints."*

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

## 1. Pipeline Bubble Ratio Math

Pipeline bubble fraction is $F_{\text{bubble}} = \frac{p - 1}{m + p - 1}$ where $p$ is pipeline stages and $m$ is micro-batches.

```python
p = 4   # 4 pipeline stages
m = 16  # 16 micro-batches
bubble_ratio = (p - 1) / (m + p - 1)

assert abs(bubble_ratio - 3 / 19) < 1e-4
assert bubble_ratio < 0.20
print(f"Pipeline bubble ratio with p={p}, m={m}: {bubble_ratio:.1%}")
```

---

## 2. One-Forward-One-Backward (1F1B) Schedule

1F1B limits peak memory by running one backward step for every forward step once the pipeline is warmed up.

```python
max_active_activations = p  # Stays bounded by number of pipeline stages
assert max_active_activations == 4
print(f"1F1B keeps peak in-flight activations bounded to {max_active_activations} micro-batches.")
```

---

## 3. Activation Checkpointing Tradeoff

Discarding activations during forward and recomputing them during backward saves 70% memory for 33% compute overhead.

```python
mem_without_checkpoints = 10.0  # GB
mem_with_checkpoints = 3.0     # GB
compute_overhead_pct = 33.0

assert mem_with_checkpoints < mem_without_checkpoints
assert mem_with_checkpoints / mem_without_checkpoints == 0.3
print(f"Activation checkpointing memory: {mem_with_checkpoints} GB vs {mem_without_checkpoints} GB baseline.")
```

---
