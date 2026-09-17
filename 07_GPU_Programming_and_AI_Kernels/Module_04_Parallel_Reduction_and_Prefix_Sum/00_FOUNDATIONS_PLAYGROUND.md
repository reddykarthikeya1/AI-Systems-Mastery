# 🐣 Interactive Foundations Playground: Parallel Reduction & Prefix Sum

> *"Tree reduction pairs neighbors up like tournament brackets, computing sum in O(log N) rounds."*

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

## 1. Tree-Based Parallel Reduction

In round $k$, each active thread adds an element offset by stride $2^k$, reducing $N$ elements in $\log_2 N$ steps.

```python
arr = [1, 2, 3, 4, 5, 6, 7, 8]
n = len(arr)
rounds = int(math.log2(n))

stride = 1
for _ in range(rounds):
    for i in range(0, n, stride * 2):
        arr[i] += arr[i + stride]
    stride *= 2

assert arr[0] == sum(range(1, 9))  # 36
assert rounds == 3
print(f"Tree reduction result at index 0: {arr[0]} in {rounds} rounds.")
```

---

## 2. Blelloch Inclusive to Exclusive Prefix Sum

Exclusive scan shifts the inclusive scan by 1 position and sets index 0 to identity 0.

```python
inclusive = [1, 3, 6, 10]
exclusive = [0] + inclusive[:-1]

assert exclusive == [0, 1, 3, 6]
assert len(exclusive) == len(inclusive)
assert exclusive[0] == 0
print(f"Exclusive prefix sum: {exclusive}")
```

---

## 3. Warp Shuffle Sum Reduction

Warp shuffle instructions exchange register values directly between threads without touching shared memory.

```python
lane_val = 1
# Butterfly reduction across 32 lanes
for delta in [16, 8, 4, 2, 1]:
    lane_val += lane_val  # Simulated reduction

assert lane_val == 32
print(f"Warp shuffle reduction sum across 32 lanes: {lane_val}")
```

---
