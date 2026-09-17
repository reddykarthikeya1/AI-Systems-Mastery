# 🐣 Interactive Foundations Playground: Greedy Algorithms & Interval Scheduling

> *"A greedy algorithm picks the best immediate option in front of it and never second-guesses."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Earliest Finish Time Interval Scheduling

Sorting intervals by end time and greedily accepting the next interval that does not overlap with the previously accepted interval maximizes total non-overlapping intervals.

```python
intervals = [(1, 4), (2, 3), (3, 5), (0, 6), (5, 7), (6, 9)]
intervals.sort(key=lambda x: x[1])

selected = []
last_end = float('-inf')
for start, end in intervals:
    if start >= last_end:
        selected.append((start, end))
        last_end = end

assert len(selected) == 3
assert selected == [(2, 3), (3, 5), (5, 7)]
print(f"Max non-overlapping intervals: {selected}")
```

---

## 2. Jump Game Maximum Reach Frontier

At each index $i$, update the farthest reachable index $\text{farthest} = \max(\text{farthest}, i + \text{nums}[i])$. If $i > \text{farthest}$, the destination is unreachable.

```python
def can_jump(nums):
    farthest = 0
    for i, x in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + x)
        if farthest >= len(nums) - 1:
            return True
    return farthest >= len(nums) - 1

assert can_jump([2, 3, 1, 1, 4]) is True
assert can_jump([3, 2, 1, 0, 4]) is False
assert can_jump([0]) is True
print("Jump game reachability verified.")
```

---

## 3. Greedy Coin Change for Canonical Systems

For canonical denominations like standard currency (25, 10, 5, 1), the greedy choice of taking the largest coin first is provably optimal.

```python
def greedy_change(amount, coins=[25, 10, 5, 1]):
    used = {}
    for c in coins:
        count = amount // c
        if count > 0:
            used[c] = count
            amount %= c
    return used

change = greedy_change(41)
assert change == {25: 1, 10: 1, 5: 1, 1: 1}
assert sum(k * v for k, v in change.items()) == 41
print(f"Greedy change for 41 cents: {change}")
```

---
