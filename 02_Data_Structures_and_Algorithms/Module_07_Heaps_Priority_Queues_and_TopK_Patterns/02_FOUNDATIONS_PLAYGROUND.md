# 🐣 Interactive Foundations Playground: Heaps (Priority Queues)

> *"A Min-Heap is like an ER hospital triage: the most urgent patient is always at the front of the line."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---


## Interactive Algorithm Trace Scrubber

```trace
{
  "title": "Min-Heap Sift-Down Invariant Scrubber",
  "algorithm": "Binary Heap Sift-Down",
  "timeComplexity": "O(log n)",
  "spaceComplexity": "O(1)",
  "frames": [
    {
      "step": 1,
      "description": "Root has invalid high value 50 after extracting min. Needs sift-down.",
      "array": [50, 4, 7, 12, 15, 20, 30],
      "pointers": { "parent": 0, "smallestChild": 1 },
      "highlights": { "0": "pivot", "1": "active", "2": "comparing" },
      "variables": { "parentVal": 50, "leftVal": 4, "rightVal": 7, "swapWith": 4 },
      "invariants": "Left child 4 is smaller than right child 7 and parent 50 -> Swap parent with 4"
    },
    {
      "step": 2,
      "description": "Swapped 50 and 4. Current parent index is 1. Check children 12 and 15.",
      "array": [4, 50, 7, 12, 15, 20, 30],
      "pointers": { "parent": 1, "smallestChild": 3 },
      "highlights": { "1": "pivot", "3": "active", "4": "comparing" },
      "variables": { "parentVal": 50, "leftVal": 12, "rightVal": 15, "swapWith": 12 },
      "invariants": "Child 12 is smaller than parent 50 -> Swap parent with 12"
    },
    {
      "step": 3,
      "description": "Swapped 50 and 12. Parent index 3 is now a leaf node. Heap property fully restored!",
      "array": [4, 12, 7, 50, 15, 20, 30],
      "pointers": { "parent": 3 },
      "highlights": { "0": "sorted", "1": "sorted", "2": "sorted", "3": "sorted" },
      "variables": { "parentVal": 50, "heapPropertyRestored": true },
      "invariants": "Min-heap invariant holds: parent <= all children"
    }
  ]
}
```

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