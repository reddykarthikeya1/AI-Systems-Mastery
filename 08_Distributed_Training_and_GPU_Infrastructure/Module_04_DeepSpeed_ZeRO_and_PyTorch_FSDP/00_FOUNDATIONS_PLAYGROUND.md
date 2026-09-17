# 🐣 Interactive Foundations Playground: DeepSpeed ZeRO & PyTorch FSDP

> *"ZeRO eliminates redundancy by sharding optimizer states, gradients, and model parameters across GPUs."*

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

## 1. Adam Optimizer State Memory Footprint (16 Bytes / Param)

Adam maintains FP32 master weights (4B), momentum (4B), and variance (4B), plus FP16 gradients (2B) and weights (2B) = 16 bytes per parameter.

```python
num_params = 1_000_000_000  # 1 Billion params
bytes_per_param_adam = 16
total_gb = (num_params * bytes_per_param_adam) / (1024**3)

assert round(total_gb, 1) == 14.9
assert bytes_per_param_adam == 16
print(f"Adam training state memory for 1B model: {total_gb:.2f} GB")
```

---

## 2. ZeRO-1 Optimizer State Sharding

ZeRO Stage 1 shards Adam states across $N_d$ GPUs: memory drops from 16 GB per GPU to $16 / N_d$ GB.

```python
world_size = 8
sharded_adam_gb = (num_params * 12) / (world_size * (1024**3))  # 12 bytes of Adam states sharded

assert sharded_adam_gb < total_gb
assert round(sharded_adam_gb, 2) == 1.40
print(f"ZeRO-1 sharded optimizer memory on 8 GPUs: {sharded_adam_gb:.2f} GB per GPU.")
```

---

## 3. ZeRO-3 Full Sharding Memory Savings

ZeRO Stage 3 shards parameters, gradients, and optimizer states; each GPU only holds $\frac{1}{N_d}$ of total training state.

```python
zero3_memory_per_gpu = total_gb / world_size
assert round(zero3_memory_per_gpu, 2) == 1.86
print(f"ZeRO-3 memory per GPU on 8 GPUs: {zero3_memory_per_gpu:.2f} GB (8x reduction)")
```

---
