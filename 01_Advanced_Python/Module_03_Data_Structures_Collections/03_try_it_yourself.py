"""Beginner playground for Module 03 - Data Structures & Collections.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque

# -------------------------------------------- 1. Double-Ended Queues for O(1) Push and Pop
d = deque([1, 2, 3], maxlen=3)
d.append(4)
assert list(d) == [2, 3, 4]
d.appendleft(10)
assert list(d) == [10, 2, 3]
assert len(d) == 3
print(f"Deque bounded buffer maintained state: {list(d)}")

# -------------------------------------------- 2. Frequency Counting with Counter
text = "banana"
counts = Counter(text)
assert counts["a"] == 3
assert counts["b"] == 1
assert counts.most_common(1)[0] == ("a", 3)
print(f"Most frequent character: {counts.most_common(1)}")

# -------------------------------------------- 3. Defaultdict Dynamic Grouping
groups = defaultdict(list)
pairs = [("odd", 1), ("even", 2), ("odd", 3), ("even", 4)]
for k, v in pairs:
    groups[k].append(v)

assert groups["odd"] == [1, 3]
assert groups["even"] == [2, 4]
assert len(groups) == 2
print(f"Defaultdict accumulated categories: {dict(groups)}")

print()
print("All checks passed.")
