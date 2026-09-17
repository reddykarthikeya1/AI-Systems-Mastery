# 🐣 Interactive Foundations Playground: KV Cache Memory Management

> *"The KV cache is a browser history of past tokens: never recompute the past, store it in GPU memory."*

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

## 1. KV Cache Bytes per Token Formula

For each token, each layer stores Key and Value vectors: $\text{Bytes} = 2 \times 2 \times n_{\text{layers}} \times n_{\text{heads}} \times d_{\text{head}} \times \text{precision}$.

```python
n_layers = 32
n_heads = 32
d_head = 128
bytes_per_elem = 2  # FP16

# 2 for Key and Value
bytes_per_token = 2 * n_layers * n_heads * d_head * bytes_per_elem

assert bytes_per_token == 524_288  # Exactly 0.5 MB per token!
assert bytes_per_token == 512 * 1024
print(f"KV Cache memory footprint: {bytes_per_token / 1024:.0f} KB per token.")
```

---

## 2. Multi-Query (MQA) and Grouped-Query (GQA) Savings

GQA groups multiple Query heads to share single Key/Value heads, slashing KV cache memory by factor $G$.

```python
num_query_heads = 32
num_kv_heads_gqa = 8  # Group of 4
gqa_ratio = num_query_heads / num_kv_heads_gqa
gqa_bytes_per_token = bytes_per_token / gqa_ratio

assert gqa_ratio == 4.0
assert gqa_bytes_per_token == 131_072  # 128 KB per token
print(f"GQA (4:1) cuts KV cache from {bytes_per_token / 1024:.0f} KB down to {gqa_bytes_per_token / 1024:.0f} KB per token.")
```

---

## 3. Maximum Sequence Capacity Calculation

Given remaining GPU VRAM after loading model weights, compute the maximum supported concurrent context tokens.

```python
available_vram_gb = 40.0
total_tokens_capacity = (available_vram_gb * (1024**3)) / gqa_bytes_per_token

assert total_tokens_capacity > 300_000
assert int(total_tokens_capacity) == 327_680
print(f"Supported KV capacity: {int(total_tokens_capacity):,} tokens across all concurrent sessions.")
```

---
