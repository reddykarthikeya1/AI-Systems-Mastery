"""Beginner playground for Module 04 - Stacks, Queues & Monotonic Structures.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import deque

# -------------------------------------------- 1. LIFO Stack and Parentheses Matching
def is_valid_parentheses(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in pairs.values():
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return len(stack) == 0

assert is_valid_parentheses("({[]})") is True
assert is_valid_parentheses("([)]") is False
assert is_valid_parentheses("(") is False
print("Parentheses matcher validated all test patterns.")

# -------------------------------------------- 2. FIFO Queue with collections.deque
queue = deque([10, 20, 30])
queue.append(40)
first = queue.popleft()
second = queue.popleft()

assert first == 10
assert second == 20
assert list(queue) == [30, 40]
print(f"Popped from queue: {first}, {second}; remaining: {list(queue)}")

# -------------------------------------------- 3. Monotonic Stack for Next Greater Element
nums = [2, 1, 2, 4, 3]
res = [-1] * len(nums)
stack = []  # indices of decreasing elements
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:
        res[stack.pop()] = x
    stack.append(i)

assert res == [4, 2, 4, -1, -1]
assert res[0] == 4 and res[1] == 2
print(f"Input: {nums} -> Next Greater Elements: {res}")

print()
print("All checks passed.")
