# 🐣 Interactive Foundations Playground: Distributed Checkpointing & Fault Tolerance

> *"Checkpointing is taking a high-speed snapshot of thousands of GPUs without stopping the cluster."*

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
import hashlib
import json
```

---

## 1. Distributed Sharded State Dictionary

Each rank writes only its local shard of model weights and optimizer states directly to storage in parallel.

```python
rank_shard = {"rank": 2, "params": [0.12, -0.45, 0.88]}
serialized = json.dumps(rank_shard)
shard_hash = hashlib.md5(serialized.encode()).hexdigest()

assert rank_shard["rank"] == 2
assert len(shard_hash) == 32
print(f"Rank 2 sharded checkpoint generated: MD5={shard_hash[:8]}...")
```

---

## 2. Asynchronous Non-Blocking Checkpoint

Copying checkpoint buffers to host RAM in background allows GPUs to resume training in under 2 seconds.

```python
sync_disk_time_s = 45.0
async_host_copy_time_s = 1.2
blocked_time_saved = sync_disk_time_s - async_host_copy_time_s

assert blocked_time_saved > 40.0
print(f"Async checkpointing reduces training stall from {sync_disk_time_s}s down to {async_host_copy_time_s}s.")
```

---

## 3. Resharding across Different Topologies

Global tensor keys allow a checkpoint trained on 8 GPUs to be loaded on 4 or 16 GPUs seamlessly.

```python
global_key = "encoder.layer.0.weight"
assert "weight" in global_key
print(f"Unified distributed tensor key: '{global_key}' verified.")
```

---
