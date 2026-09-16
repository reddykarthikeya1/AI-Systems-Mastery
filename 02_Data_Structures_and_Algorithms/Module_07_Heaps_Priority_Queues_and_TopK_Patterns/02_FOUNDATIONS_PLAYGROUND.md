# 🐣 Interactive Foundations Playground: Heaps (Priority Queues)

> *"A Min-Heap is like an ER hospital triage: the most urgent patient is always at the front of the line."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

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
