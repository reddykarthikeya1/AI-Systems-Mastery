# 🐣 Interactive Foundations Playground: Continuous & Dynamic Batching

> *"Continuous batching is a subway train: open the doors at every station to let finished passengers off and new ones on."*

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
from collections import deque
```

---

## 1. Iteration-Level Scheduling vs Static Batching

Static batching waits until the longest request in a batch finishes; continuous batching swaps finished requests on every iteration.

```python
active_requests = {"req_1": 2, "req_2": 5, "req_3": 1}  # Remaining tokens
finished = []

# One decode iteration
for rid in list(active_requests.keys()):
    active_requests[rid] -= 1
    if active_requests[rid] == 0:
        finished.append(rid)
        del active_requests[rid]

assert finished == ["req_3"]
assert "req_1" in active_requests and "req_2" in active_requests
print(f"Iteration finished requests: {finished}; slots immediately freed for new arrivals.")
```

---

## 2. Padding Token Elimination

Continuous batching concatenates active tokens into a 1D flattened buffer without inserting pad tokens.

```python
seq_lengths = [3, 5, 2]
static_padded_matrix_elements = max(seq_lengths) * len(seq_lengths)  # 5 * 3 = 15
continuous_flattened_elements = sum(seq_lengths)                     # 10
tokens_saved = static_padded_matrix_elements - continuous_flattened_elements

assert static_padded_matrix_elements == 15
assert continuous_flattened_elements == 10
assert tokens_saved == 5
print(f"Continuous batching eliminated {tokens_saved} wasteful padding tokens (33% compute saved).")
```

---

## 3. GPU Utilization Saturation

By keeping the active batch size close to maximum capacity $B_{\max}$, continuous batching achieves sustained GPU utilization.

```python
max_capacity = 8
waiting_queue = deque(["req_4", "req_5"])
while len(active_requests) < max_capacity and waiting_queue:
    active_requests[waiting_queue.popleft()] = 4

assert len(active_requests) == 4
print(f"Active batch replenished to {len(active_requests)} requests.")
```

---
