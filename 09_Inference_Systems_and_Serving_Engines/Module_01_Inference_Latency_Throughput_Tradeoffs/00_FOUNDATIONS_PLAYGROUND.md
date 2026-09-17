# 🐣 Interactive Foundations Playground: Inference Latency vs Throughput Tradeoffs

> *"TTFT is how quickly the waiter brings your appetizer; TPOT is how fast they serve the rest of the courses."*

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

## 1. Time to First Token (TTFT) vs Time Per Output Token (TPOT)

Total response latency equals TTFT (prefill phase processing prompt tokens) plus TPOT times generated tokens (decode phase).

```python
prompt_tokens = 500
gen_tokens = 100
prefill_rate = 2000.0  # tokens/sec
decode_rate = 50.0     # tokens/sec (per token TPOT = 20ms)

ttft_sec = prompt_tokens / prefill_rate   # 0.25s
tpot_sec = 1.0 / decode_rate             # 0.02s
total_latency_sec = ttft_sec + gen_tokens * tpot_sec

assert ttft_sec == 0.25
assert tpot_sec == 0.02
assert total_latency_sec == 2.25
print(f"TTFT: {ttft_sec*1000:.0f} ms, TPOT: {tpot_sec*1000:.0f} ms, Total Latency: {total_latency_sec:.2f} s")
```

---

## 2. Prefill (Compute-Bound) vs Decode (Memory-Bound)

Prefill processes all prompt tokens in parallel with high arithmetic intensity; decode processes one token per step, limited by memory bandwidth.

```python
model_weights_gb = 14.0  # 7B model in FP16
hbm_bw_gb_s = 2000.0     # H100 HBM3 bandwidth
min_decode_step_sec = model_weights_gb / hbm_bw_gb_s  # 7 ms per token

max_single_stream_tps = 1.0 / min_decode_step_sec
assert round(max_single_stream_tps, 1) == 142.9
assert min_decode_step_sec == 0.007
print(f"Single-stream decode upper bound: {max_single_stream_tps:.1f} tokens/s (step: {min_decode_step_sec*1000:.1f} ms)")
```

---

## 3. Batching Throughput Multiplication

Batching amortizes the cost of reading model weights across multiple concurrent requests, multiplying system throughput.

```python
batch_size = 16
tokens_per_step = batch_size
batch_throughput_tps = tokens_per_step / min_decode_step_sec

assert batch_throughput_tps > max_single_stream_tps
assert round(batch_throughput_tps) == 2286
print(f"Batching {batch_size} streams increases throughput to {batch_throughput_tps:.0f} tokens/s.")
```

---
