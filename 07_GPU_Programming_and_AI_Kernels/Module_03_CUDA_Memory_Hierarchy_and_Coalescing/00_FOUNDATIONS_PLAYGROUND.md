# 🐣 Interactive Foundations Playground: CUDA Memory Hierarchy & Coalescing

> *"Global memory is a distant warehouse; Shared memory is a workbench right at your fingertips."*

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

## 1. Memory Latency Hierarchy

Registers take 1 cycle, Shared Memory takes ~20 cycles, and Global DRAM takes ~200-400 cycles.

```python
latencies = {"registers": 1, "shared_sram": 20, "global_dram": 300}
assert latencies["global_dram"] / latencies["registers"] == 300
assert latencies["shared_sram"] < latencies["global_dram"]
print(f"Memory latencies in cycles: {latencies}")
```

---

## 2. Coalesced Memory Access Pattern

When 32 consecutive threads access 32 consecutive 4-byte words, the GPU services the request in a single 128-byte transaction.

```python
warp_size = 32
bytes_per_word = 4
transaction_size = 128  # bytes

# Coalesced: thread i accesses index i
coalesced_span = warp_size * bytes_per_word
transactions_needed = math.ceil(coalesced_span / transaction_size)

assert coalesced_span == 128
assert transactions_needed == 1
print(f"Coalesced warp access requires exactly {transactions_needed} memory transaction(s).")
```

---

## 3. Strided Uncoalesced Memory Penalty

Accessing memory with stride $S > 1$ scatters memory requests across multiple transaction cache lines, wasting bandwidth.

```python
stride = 8
uncoalesced_span = warp_size * bytes_per_word * stride
transactions_strided = min(warp_size, math.ceil(uncoalesced_span / transaction_size))

assert transactions_strided > transactions_needed
assert transactions_strided == 8
print(f"Strided access (stride={stride}) burns {transactions_strided} transactions for same data.")
```

---
