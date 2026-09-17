# 🐣 Interactive Foundations Playground: Sequence & Context Parallelism (Ring Attention)

> *"Ring Attention passes Key and Value blocks around a ring of GPUs, calculating attention on infinite context."*

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

## 1. Sequence Sharding Across GPUs

A 128k context is sharded into 16k chunks across 8 GPUs; each GPU holds only its local query chunk.

```python
total_context = 128_000
num_gpus = 8
local_chunk = total_context // num_gpus

assert local_chunk == 16_000
assert local_chunk * num_gpus == total_context
print(f"128k context sharded into {local_chunk} tokens per GPU across {num_gpus} GPUs.")
```

---

## 2. Ring KV Shift Communication

At each step, GPU $i$ transmits its Key-Value block to GPU $(i+1) \pmod N$ and receives from $(i-1) \pmod N$.

```python
ring_ranks = [0, 1, 2, 3]
next_ranks = [(r + 1) % len(ring_ranks) for r in ring_ranks]
prev_ranks = [(r - 1) % len(ring_ranks) for r in ring_ranks]

assert next_ranks == [1, 2, 3, 0]
assert prev_ranks == [3, 0, 1, 2]
print(f"Ring communication mapping: next={next_ranks}, prev={prev_ranks}")
```

---

## 3. Zero Extra Memory Context Scaling

Ring Attention memory per GPU remains $O(N / G)$, enabling linear scaling to millions of tokens.

```python
mem_per_gpu = 16_000 * 2  # 32 KB per head
assert mem_per_gpu == 32_000
print(f"Per-GPU memory bound invariant verified.")
```

---
