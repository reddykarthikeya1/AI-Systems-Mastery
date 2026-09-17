# 🐣 Interactive Foundations Playground: Distributed Data Parallel (DDP)

> *"DDP gives each GPU a copy of the model, feeds them different batches, and averages their gradients."*

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

## 1. Gradient Averaging Across Ranks

Each rank computes gradients on local micro-batch; AllReduce computes the global mean gradient: $\bar{g} = \frac{1}{W} \sum g_w$.

```python
grad_gpu0 = [0.2, 0.4]
grad_gpu1 = [0.4, 0.8]
world_size = 2

avg_grad = [(g0 + g1) / world_size for g0, g1 in zip(grad_gpu0, grad_gpu1)]
assert abs(avg_grad[0] - 0.3) < 1e-6 and abs(avg_grad[1] - 0.6) < 1e-6
assert len(avg_grad) == 2
print(f"Synchronized average gradients: {avg_grad}")
```

---

## 2. Gradient Bucketing to Overlap Compute and Comm

DDP groups small parameter gradients into 25 MB contiguous buckets so AllReduce fires while backward pass computes earlier layers.

```python
bucket_size_mb = 25.0
param_grads = [5.0, 12.0, 10.0, 8.0]  # Sizes in MB
buckets = []
current_bucket = 0.0

for g in param_grads:
    if current_bucket + g > bucket_size_mb:
        buckets.append(current_bucket)
        current_bucket = g
    else:
        current_bucket += g
buckets.append(current_bucket)

assert len(buckets) == 2
assert buckets[0] == 17.0  # 5 + 12
assert buckets[1] == 18.0  # 10 + 8
print(f"Buckets formed: {buckets} MB (threshold: {bucket_size_mb} MB)")
```

---

## 3. Effective Global Batch Size Scaling

Global batch size equals $\text{per-GPU batch size} \times \text{world size} \times \text{gradient accumulation steps}$.

```python
per_device_batch = 4
world_size = 8
grad_accum = 4
global_batch = per_device_batch * world_size * grad_accum

assert global_batch == 128
print(f"Global effective batch size: {global_batch}")
```

---
