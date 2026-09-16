# Module 07: Heaps, Priority Queues & TopK Patterns (0 to 100 Mastery)

> **Complete Binary Trees, Sift-Up/Sift-Down, $O(N)$ Heapify & Streaming Quantiles**

Binary Heaps provide guaranteed $O(1)$ minimum/maximum lookup and $O(\\log N)$ insertion and deletion. In this module, you master **Bottom-Up Heapify ($O(N)$ proof)**, **Top-K Streaming Elements**, **Two-Heap Median Tracking**, and **K-Way List Merging**.

---

## 1. The $O(N)$ Bottom-Up Heapify Proof

Building a heap by inserting $N$ elements one by one takes $O(N \\log N)$.
However, bottom-up `heapify` sifts down starting at index $\\lfloor N/2 \\rfloor - 1$:
$$\\sum_{h=0}^{\\log N} \\frac{N}{2^{h+1}} \\cdot O(h) = O(N \\sum_{h=0}^\\infty \\frac{h}{2^h}) = O(2N) = O(N)$$

---

## 2. Curated LeetCode Problem Breakdowns (Brute Force vs. Optimized)

### Problem 1: Kth Largest Element in an Array ([LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/)) — Medium

#### Brute Force: Full Sort
- **Time Complexity**: $O(N \\log N)$.

#### Optimized: Min-Heap of Size K ($O(N \\log K)$ Time, $O(K)$ Space)
```python
import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```
- **Time Complexity**: $O(N \\log K)$ — Substantially faster when $K \\ll N$.
- **Space Complexity**: $O(K)$.

---

### Problem 2: Last Stone Weight ([LeetCode 1046](https://leetcode.com/problems/last-stone-weight/)) — Easy

#### Optimized: Max-Heap Simulation
Multiply by $-1$ in Python's min-heap. Pop two largest, smash, and push difference if $> 0$.
```python
import heapq

def last_stone_weight(stones: list[int]) -> int:
    h = [-s for s in stones]
    heapq.heapify(h)
    while len(h) > 1:
        s1 = -heapq.heappop(h)
        s2 = -heapq.heappop(h)
        if s1 != s2:
            heapq.heappush(h, -(s1 - s2))
    return -h[0] if h else 0
```
- **Time Complexity**: $O(N \\log N)$, **Space Complexity**: $O(N)$.

---

### Problem 3: K Closest Points to Origin ([LeetCode 973](https://leetcode.com/problems/k-closest-points-to-origin/)) — Medium

#### Optimized: Max-Heap of Size K
Maintain $K$ smallest distances in a max-heap of capacity $K$ using distance $-(x^2 + y^2)$.
- **Time Complexity**: $O(N \\log K)$, **Space Complexity**: $O(K)$.

---

### Problem 4: Task Scheduler ([LeetCode 621](https://leetcode.com/problems/task-scheduler/)) — Medium

#### Optimized: Greedy Idle Slot Math ($O(N)$ Time, $O(1)$ Space)
The most frequent task creates $(max\\_freq - 1)$ chunk frames of length $(n + 1)$.
```python
from collections import Counter

def least_interval(tasks: list[str], n: int) -> int:
    counts = Counter(tasks)
    max_f = max(counts.values())
    max_f_count = sum(1 for c in counts.values() if c == max_f)
    
    empty_slots = (max_f - 1) * (n - (max_f_count - 1))
    available_tasks = len(tasks) - (max_f * max_f_count)
    idles = max(0, empty_slots - available_tasks)
    
    return len(tasks) + idles
```
- **Time Complexity**: $O(N)$, **Space Complexity**: $O(1)$ (26 uppercase letters).

---

### Problem 5: Find Median from Data Stream ([LeetCode 295](https://leetcode.com/problems/find-median-from-data-stream/)) — Hard

#### Optimized: Two Balanced Heaps (Max-Heap + Min-Heap)
- `small`: Max-heap storing lower half of numbers.
- `large`: Min-heap storing upper half of numbers.
- Invariant: `len(small) == len(large)` or `len(small) == len(large) + 1`.
```python
import heapq

def __init__(self):
    self.small = []  # max-heap (negated)
    self.large = []  # min-heap

def add_num(self, num: int) -> None:
    heapq.heappush(self.small, -num)
    # Ensure all in small <= all in large
    if self.small and self.large and (-self.small[0] > self.large[0]):
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)
    # Balance sizes
    if len(self.small) > len(self.large) + 1:
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)
    elif len(self.large) > len(self.small):
        val = heapq.heappop(self.large)
        heapq.heappush(self.small, -val)

def find_median(self) -> float:
    if len(self.small) > len(self.large):
        return float(-self.small[0])
    return (-self.small[0] + self.large[0]) / 2.0
```
- **Time Complexity**: $O(\\log N)$ per `addNum`, $O(1)$ `findMedian`.
- **Space Complexity**: $O(N)$.

---

## 3. Hands-On Project & Test Suite

Verify your Binary Min-Heap and Top-K tracking engine:
- Starter Template: [`starter/binary_min_heap_engine.py`](starter/binary_min_heap_engine.py)
- Production Solution: [`project_solution/binary_min_heap_engine.py`](project_solution/binary_min_heap_engine.py)
- Pytest Suite: [`project_solution/test_binary_min_heap_engine.py`](project_solution/test_binary_min_heap_engine.py)

## 🧪 Practice & Verification

Reading a module teaches recognition. Only the problems teach recall — and the
debug lab teaches the thing neither of them does, which is diagnosis.

### 1. Build the module project

```bash
cd starter
python -m pytest ../project_solution -q      # must FAIL before you start
```

Every shipped test must fail with `NotImplementedError` on an untouched
starter. If any passes, the grading loop is broken and is telling you your work
is correct when it has not been done — run `make integrity` from the course
root.

### 2. Work the problem bank — 8 problems

```bash
cd problems
python -m pytest tests -q                    # all of this module's problems
python -m pytest tests -q -k p03             # just problem 3
```

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [K-th Largest Element](problems/p01_kth_largest.py) | Min-heap of size k | Medium | `Time O(n log k), Space O(k)` |
| 02 | [Merge K Sorted Lists](problems/p02_merge_k_sorted.py) | Min-heap k-way merge | Hard | `Time O(N log k), Space O(k)` |
| 03 | [Median From A Data Stream](problems/p03_streaming_median.py) | Two heaps | Hard | `Time O(n log n) total, O(1) per query, Space O(n)` |
| 04 | [K Closest Points To The Origin](problems/p04_k_closest_points.py) | Max-heap of size k | Medium | `Time O(n log k), Space O(k)` |
| 05 | [Last Stone Weight](problems/p05_last_stone_weight.py) | Max-heap simulation | Easy | `Time O(n log n), Space O(n)` |
| 06 | [Minimum Meeting Rooms](problems/p06_min_meeting_rooms.py) | Heap of end times | Medium | `Time O(n log n), Space O(n)` |
| 07 | [Task Scheduler With Cooldown](problems/p07_task_scheduler.py) | Greedy counting (heap-free) | Medium | `Time O(n), Space O(alphabet)` |
| 08 | [Reorganize String](problems/p08_reorganize_string.py) | Greedy with a max-heap | Hard | `Time O(n log 26), Space O(n)` |

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Every reference solution in `problems/solutions/` is cross-checked against
a brute force or a second implementation, so the answers are verified rather
than asserted.

### 3. Work the debug lab

```bash
cd debug_lab
python broken_priority_toolkit.py
echo "exit=$?"
```

It exits 0 and prints wrong answers. Read [`SYMPTOMS.md`](debug_lab/SYMPTOMS.md),
write a diagnosis for each, and only then open `ANSWERS.md`. The diagnostic
reasoning is the transferable skill; reading the answer first skips it.

---

## ✅ You have mastered this module when you can…

1. Explain why the k LARGEST elements are kept in a MIN-heap of size k.
2. Maintain a streaming median with two heaps, and state the size invariant that makes it work.
3. Recognise k-way merge, top-k and scheduling as heap problems from their phrasing.
4. Say when a heap is the wrong tool because a counting or bucket approach is O(n).

Each of these is something you **do**, not something you know. If you cannot do
one without reference, that is the section to revisit — not the whole module.

---

## 🧭 Navigation

- [Pattern Recognition Guide](../PATTERN_RECOGNITION_GUIDE.md) — how to attack a problem you have never seen
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md)
- [Problem bank](problems/README.md) · [Debug lab](debug_lab/SYMPTOMS.md)
