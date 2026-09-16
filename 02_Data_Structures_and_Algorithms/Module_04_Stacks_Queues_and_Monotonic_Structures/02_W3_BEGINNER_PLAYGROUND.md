# 🐣 W3Schools-Style Playground: Stacks & Queues

> *"A stack is a stack of pancakes. A queue is a line at Starbucks."*

---

## 1. Stack = LIFO (Last-In, First-Out)
- The **last** pancake put on the plate is the **first** pancake eaten!
- In Python: Use a simple list with `.append()` and `.pop()`. Both run in instant $O(1)$ time!

```python
stack = []
stack.append("Page 1")
stack.append("Page 2")
print(stack.pop()) # "Page 2" (Just like browser Back button!)
```

---

## 2. Queue = FIFO (First-In, First-Out)
- The **first** person to join the Starbucks line gets coffee first!
- In Python: Always use `collections.deque`! A standard list `.pop(0)` is slow ($O(N)$) because it shifts all remaining elements.

```python
from collections import deque
queue = deque(["Alice", "Bob", "Charlie"])
print(queue.popleft()) # "Alice" (Fast O(1) removal!)
```
