# 🐣 Interactive Foundations Playground: Heaps (Priority Queues)

> *"A Min-Heap is like an ER hospital triage: the most urgent patient is always at the front of the line."*

---

## 1. How Python's `heapq` Works
In Python, `heapq` turns any normal list into a Min-Heap:
```python
import heapq

pq = []
heapq.heappush(pq, 50)
heapq.heappush(pq, 10) # 10 jumps to the front!
heapq.heappush(pq, 30)

print(heapq.heappop(pq)) # 10 (Smallest popped first!)
```
