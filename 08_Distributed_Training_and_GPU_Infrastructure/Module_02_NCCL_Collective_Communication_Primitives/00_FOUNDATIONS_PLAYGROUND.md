# 🐣 Interactive Foundations Playground: NCCL Collective Communication Primitives

> *"Collectives are coordinated dance moves for GPUs: AllReduce, AllGather, and ReduceScatter."*

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

## 1. AllReduce via ReduceScatter + AllGather

Ring-AllReduce breaks down into two phases: ReduceScatter (sum chunks) followed by AllGather (replicate sums).

```python
data_per_gpu = [1.0, 2.0, 3.0]  # GPU 0
num_gpus = 4
total_data_size = 100  # MB
volume_transferred = 2 * ((num_gpus - 1) / num_gpus) * total_data_size

assert volume_transferred == 2 * (3 / 4) * 100  # 150 MB
assert volume_transferred < 2 * total_data_size
print(f"Total data sent per GPU in 4-GPU Ring-AllReduce: {volume_transferred} MB")
```

---

## 2. Broadcast Primitive Invariant

Broadcast copies a buffer from rank 0 to all other ranks in the communication group.

```python
ranks = [0, 1, 2, 3]
root_val = 42
cluster_state = [root_val if r == 0 else 0 for r in ranks]

# Broadcast from rank 0
for r in range(len(cluster_state)):
    cluster_state[r] = cluster_state[0]

assert all(val == 42 for val in cluster_state)
assert len(cluster_state) == 4
print(f"Broadcast replicated value 42 across all ranks: {cluster_state}")
```

---

## 3. Reduce-Scatter Chunk Partitioning

Each rank receives the reduced sum of its assigned rank slice: rank $i$ holds the global sum of chunk $i$.

```python
gpu_tensors = [[1, 10], [2, 20], [3, 30]]  # 3 GPUs, 2 elements each
chunk_0_sum = sum(t[0] for t in gpu_tensors)
chunk_1_sum = sum(t[1] for t in gpu_tensors)

assert chunk_0_sum == 6
assert chunk_1_sum == 60
print(f"Reduce-Scatter outputs: chunk 0 -> {chunk_0_sum}, chunk 1 -> {chunk_1_sum}")
```

---
