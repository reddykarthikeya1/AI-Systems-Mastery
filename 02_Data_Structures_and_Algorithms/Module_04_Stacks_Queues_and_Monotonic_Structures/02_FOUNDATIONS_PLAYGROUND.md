# 🐣 Interactive Foundations Playground: Stacks, Queues & Monotonic Structures

> *"A stack is a stack of dirty plates (LIFO); a queue is a line at the supermarket (FIFO)."*

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
from collections import deque
```

---

## 1. LIFO Stack and Parentheses Matching

Pushing opening brackets onto a stack and popping when matching closing brackets occur verifies nested syntactic validity in $O(N)$ time.

```python
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
```

---

## 2. FIFO Queue with collections.deque

Python's `collections.deque` provides $O(1)$ append and popleft operations from both ends, avoiding the $O(N)$ shift cost of list pops.

```python
queue = deque([10, 20, 30])
queue.append(40)
first = queue.popleft()
second = queue.popleft()

assert first == 10
assert second == 20
assert list(queue) == [30, 40]
print(f"Popped from queue: {first}, {second}; remaining: {list(queue)}")
```

---

## 3. Monotonic Stack for Next Greater Element

Maintaining a stack of indices with decreasing values allows finding the next greater element for every index in $O(N)$ total time.

```python
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
```

---
