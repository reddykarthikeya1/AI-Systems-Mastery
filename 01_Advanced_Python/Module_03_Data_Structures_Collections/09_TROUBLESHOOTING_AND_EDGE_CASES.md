# Module 03: Troubleshooting, Common Traps & Edge Cases in Data Structures

This guide details common bugs, performance hazards, and edge cases when working with lists, dictionaries, sets, and specialized collections in Python.

---

## 1. Modifying a List While Iterating Over It

### The Bug
```python
numbers = [1, 2, 3, 4, 5, 6]

# Goal: Remove all even numbers
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)

print(numbers)  # [1, 3, 5, 6]  <-- 6 was skipped!
```

### Why It Happens
Python tracks your position using an internal integer index ($0, 1, 2...$). When you remove `2` at index `1`, the remaining elements shift left. In the next step, Python advances to index `2`, skipping the element that slid into index `1`!

### The Fix
1. **Use a List Comprehension (Recommended):**
   ```python
   numbers = [n for n in numbers if n % 2 != 0]
   ```
2. **Iterate over a shallow copy:**
   ```python
   for n in numbers[:]:
       if n % 2 == 0:
           numbers.remove(n)
   ```

---

## 2. `TypeError: unhashable type: 'list'` (Mutable Dictionary Keys)

### The Bug
```python
coordinates = [10, 20]
locations = {}
locations[coordinates] = "Warehouse Alpha"  # ❌ Crash!
```
**Crash:** `TypeError: unhashable type: 'list'`

### Why It Happens
Hash tables depend on keys having an unchanging hash value for instant lookup. If a list could be a key, changing `coordinates.append(30)` would change its hash, making the value lost forever in the wrong memory bucket!

### The Fix
Use an **immutable tuple** instead:
```python
coordinates = (10, 20)
locations = {}
locations[coordinates] = "Warehouse Alpha"  # ✅ Works perfectly!
```

---

## 3. The Shallow Copy Mutation Trap with Nested Structures

### The Bug
```python
grid = [[0] * 3] * 3
grid[0][0] = 1

# What does the grid look like?
print(grid)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]  <-- All 3 rows changed!
```

### Why It Happens
`[sublist] * 3` does not clone the sublist 3 times. It creates a single list and duplicates the pointer reference 3 times!

### The Fix
Use a list comprehension to create independent sublists:
```python
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
print(grid)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]  <-- Only row 0 changed!
```

---

## 4. `defaultdict` Accidental Key Creation

### The Bug
```python
from collections import defaultdict

counts = defaultdict(int)
# Check if a user exists by accessing the key:
if counts["alice"] == 0:
    pass

print(list(counts.keys()))  # ['alice']  <-- 'alice' was silently inserted!
```

### Why It Happens
Merely accessing `counts["alice"]` triggers `defaultdict` to create the key with default value `0`.

### The Fix
Use the `in` operator to check membership without inserting:
```python
if "alice" in counts:
    print("Found alice!")
```

---

## 5. `heapq` Max-Heap Inversion

### The Observation
Python's `heapq` is strictly a **Min-Heap** (smallest numbers pop first). How do you build a **Max-Heap** (highest priority first)?

### The Solution: Negate Values
Multiply numerical values by `-1`:
```python
import heapq

max_heap = []
# Store bid orders where highest price is top priority:
heapq.heappush(max_heap, (-105.50, "Bid Order #1"))
heapq.heappush(max_heap, (-110.00, "Bid Order #2"))

highest_bid_neg, order_id = heapq.heappop(max_heap)
highest_bid = -highest_bid_neg
print(f"Top Bid: ${highest_bid:.2f} for {order_id}")  # $110.00
```
