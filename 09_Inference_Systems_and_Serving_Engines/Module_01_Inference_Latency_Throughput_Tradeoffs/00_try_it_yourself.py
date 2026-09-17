"""Beginner playground for Module 01 - Inference Latency vs Throughput Tradeoffs.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Time to First Token (TTFT) vs Time Per Output Token (TPOT)
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

# -------------------------------------------- 2. Prefill (Compute-Bound) vs Decode (Memory-Bound)
model_weights_gb = 14.0  # 7B model in FP16
hbm_bw_gb_s = 2000.0     # H100 HBM3 bandwidth
min_decode_step_sec = model_weights_gb / hbm_bw_gb_s  # 7 ms per token

max_single_stream_tps = 1.0 / min_decode_step_sec
assert round(max_single_stream_tps, 1) == 142.9
assert min_decode_step_sec == 0.007
print(f"Single-stream decode upper bound: {max_single_stream_tps:.1f} tokens/s (step: {min_decode_step_sec*1000:.1f} ms)")

# -------------------------------------------- 3. Batching Throughput Multiplication
batch_size = 16
tokens_per_step = batch_size
batch_throughput_tps = tokens_per_step / min_decode_step_sec

assert batch_throughput_tps > max_single_stream_tps
assert round(batch_throughput_tps) == 2286
print(f"Batching {batch_size} streams increases throughput to {batch_throughput_tps:.0f} tokens/s.")

print()
print("All checks passed.")
