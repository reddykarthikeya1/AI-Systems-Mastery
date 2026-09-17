# 🐣 Interactive Foundations Playground: Data Structures & Collections

> *"Choosing the right collection changes algorithm runtime from $O(N)$ to $O(1)$."*

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
from collections import Counter, defaultdict, deque
```

---

## 1. Double-Ended Queues for O(1) Push and Pop

Python `deque` provides $O(1)$ operations on both ends, avoiding list reallocation overhead.

```python
d = deque([1, 2, 3], maxlen=3)
d.append(4)
assert list(d) == [2, 3, 4]
d.appendleft(10)
assert list(d) == [10, 2, 3]
assert len(d) == 3
print(f"Deque bounded buffer maintained state: {list(d)}")
```

---

## 2. Frequency Counting with Counter

`Counter` computes multiset statistics and frequency intersections in a single pass.

```python
text = "banana"
counts = Counter(text)
assert counts["a"] == 3
assert counts["b"] == 1
assert counts.most_common(1)[0] == ("a", 3)
print(f"Most frequent character: {counts.most_common(1)}")
```

---

## 3. Defaultdict Dynamic Grouping

`defaultdict` eliminates boilerplate KeyError checks when accumulating groupings.

```python
groups = defaultdict(list)
pairs = [("odd", 1), ("even", 2), ("odd", 3), ("even", 4)]
for k, v in pairs:
    groups[k].append(v)

assert groups["odd"] == [1, 3]
assert groups["even"] == [2, 4]
assert len(groups) == 2
print(f"Defaultdict accumulated categories: {dict(groups)}")
```

---
