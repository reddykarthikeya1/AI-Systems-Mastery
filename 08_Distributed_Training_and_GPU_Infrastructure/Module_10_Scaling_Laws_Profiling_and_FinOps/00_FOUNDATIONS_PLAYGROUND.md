# 🐣 Interactive Foundations Playground: Scaling Laws, Profiling & FinOps

> *"Chinchilla scaling proves compute and dataset tokens must grow in equal proportion."*

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

## 1. Chinchilla Optimal Token-to-Parameter Ratio (20x)

For compute-optimal LLM training, number of tokens $D$ should equal approximately $20 \times \text{Parameters } N$.

```python
params = 7_000_000_000  # 7B model
optimal_tokens = 20 * params

assert optimal_tokens == 140_000_000_000  # 140 Billion tokens
assert optimal_tokens / params == 20
print(f"Chinchilla optimal token count for 7B model: {optimal_tokens / 1e9:.0f} Billion tokens.")
```

---

## 2. Total Training FLOPs Estimation C = 6 * N * D

Each token in forward pass costs $2N$ FLOPs; backward pass costs $4N$ FLOPs. Total training compute is $6ND$.

```python
N = 7e9
D = 140e9
total_flops = 6 * N * D

assert total_flops == 5.88e21
print(f"Total training FLOPs: {total_flops:.2e}")
```

---

## 3. Training Cost & GPU Hours Estimation

Estimating GPU cluster hours and total cloud dollar cost based on MFU and hourly node price.

```python
h100_sxm_tflops = 312e12
mfu = 0.40
effective_tflops = h100_sxm_tflops * mfu
gpu_seconds = total_flops / effective_tflops
gpu_hours = gpu_seconds / 3600
cost_at_3_per_hr = gpu_hours * 3.0

assert gpu_hours > 0
print(f"Estimated GPU hours: {gpu_hours:,.0f} hrs (~${cost_at_3_per_hr:,.2f})")
```

---
