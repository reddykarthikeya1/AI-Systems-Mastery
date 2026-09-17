# 🐣 Interactive Foundations Playground: Heaps, Priority Queues & Top-K Patterns

> *"A min-heap is a company where the lowest-ranking intern is always at the top of the stack."*

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
import heapq
```

---

## 1. Min-Heap Array Invariant

In a binary min-heap stored as an array, the item at index `0` is always the global minimum: `heap[0] <= heap[2*i + 1]` and `heap[0] <= heap[2*i + 2]`.

```python
h = [40, 10, 30, 20, 50]
heapq.heapify(h)
assert h[0] == 10, "Root must be the minimum element"
smallest = heapq.heappop(h)
assert smallest == 10
assert h[0] == 20, "Next smallest must rise to index 0"
print(f"Heapified array: {h}, extracted minimum: {smallest}")
```

---

## 2. Streaming Top-K with a Bounded Min-Heap

Maintaining a min-heap of size $K$ while processing an unbounded stream keeps the $K$ largest elements seen so far in $O(N \log K)$ time and $O(K)$ space.

```python
stream = [5, 12, 3, 25, 1, 18, 9, 30, 2]
k = 3
k_heap = []
for num in stream:
    if len(k_heap) < k:
        heapq.heappush(k_heap, num)
    elif num > k_heap[0]:
        heapq.heapreplace(k_heap, num)

top_k = sorted(k_heap, reverse=True)
assert top_k == [30, 25, 18], "Top 3 numbers in stream"
assert len(k_heap) == 3
print(f"Top {k} numbers in stream: {top_k}")
```

---

## 3. Max-Heap Emulation using Negation

Python's `heapq` is min-heap only. Negating values on insert and re-negating on pop emulates a max-heap cleanly without third-party libraries.

```python
max_h = []
for x in [10, 50, 20, 40]:
    heapq.heappush(max_h, -x)

largest = -heapq.heappop(max_h)
second_largest = -heapq.heappop(max_h)
assert largest == 50
assert second_largest == 40
print(f"Max-heap extracted in descending order: {largest}, {second_largest}")
```

---
