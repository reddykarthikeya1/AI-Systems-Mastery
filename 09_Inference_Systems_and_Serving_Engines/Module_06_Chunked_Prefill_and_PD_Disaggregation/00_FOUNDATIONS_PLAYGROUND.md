# 🐣 Interactive Foundations Playground: Chunked Prefill & PD Disaggregation

> *"Prefill-Decode disaggregation separates the sprint (prefill) from the marathon (decode) onto dedicated GPUs."*

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

## 1. Chunked Prefill Token Budgeting

Chunked prefill splits large prompts into chunks of size $B$ (e.g. 512 tokens), interleaving prompt processing with ongoing decode steps.

```python
prompt_size = 1200
chunk_budget = 512
chunks = []
remaining = prompt_size
while remaining > 0:
    c = min(remaining, chunk_budget)
    chunks.append(c)
    remaining -= c

assert chunks == [512, 512, 176]
assert sum(chunks) == 1200
print(f"Prompt chunked into steps: {chunks}")
```

---

## 2. Decoupled Inter-GPU KV Transfer

In PD Disaggregation, dedicated Prefill nodes compute KV cache and ship it across 400 Gbps network to Decode nodes.

```python
kv_cache_mb = 64.0
network_bw_gb_s = 50.0  # 400 Gbps InfiniBand
transfer_time_ms = (kv_cache_mb / (network_bw_gb_s * 1024)) * 1000

assert transfer_time_ms < 2.0
assert transfer_time_ms == 1.25
print(f"KV transfer time across network: {transfer_time_ms:.2f} ms (negligible latency).")
```

---

## 3. Elimination of Decode Interference

Prefill bursts no longer interrupt decoding iterations, stabilizing TPOT at consistent low percentiles.

```python
tpot_without_disaggregation = [20, 21, 150, 20, 180]  # Spikes due to prefill preemption
tpot_with_disaggregation = [20, 21, 20, 21, 20]        # Smooth execution

assert max(tpot_with_disaggregation) == 21
assert max(tpot_without_disaggregation) == 180
print(f"P99 TPOT reduced from {max(tpot_without_disaggregation)} ms to {max(tpot_with_disaggregation)} ms.")
```

---
