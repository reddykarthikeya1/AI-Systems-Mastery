# 🐣 Interactive Foundations Playground: Stacks & Queues

> *"A stack is a stack of pancakes. A queue is a line at Starbucks."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

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
