# Module 03: Data Structures – Organizing Data Efficiently

Welcome to **Module 03**! In this module, we will demystify how Python stores, organizes, and searches through collections of data. We'll explore **Lists**, **Tuples**, **Dictionaries (Hash Tables)**, **Sets**, **Big-$O$ Time Complexity**, the specialized **`collections`** module (`deque`, `Counter`, `defaultdict`), and **Priority Heaps (`heapq`)**.

---

## 1. What is a Data Structure? The Kitchen Storage Analogy

Imagine you are organizing a commercial kitchen:
* **The Egg Carton (Lists):** Eggs sit in ordered slots (Slot 0, Slot 1, Slot 2). You can access any egg instantly by its position, but inserting an egg into the middle shifts every other egg down.
* **The Spice Rack with Labels (Dictionaries):** Every spice jar has a unique labeled name tag (e.g. `"cinnamon"`). You don't count slots; you look up `"cinnamon"` directly.
* **The Unique Ingredient Bowl (Sets):** A bowl that refuses duplicates. If you drop a second pinch of salt, it merges into the salt already there.

Choosing the right container determines whether your program runs in **0.001 seconds** or **10 minutes**.

---

## 2. Big-$O$ Complexity Made Simple

Big-$O$ notation measures **how the running time or memory usage of an algorithm scales as the amount of data ($N$) grows**:

| Notation | Name | Real-World Intuition | Example in Python |
| :--- | :--- | :--- | :--- |
| **$O(1)$** | **Constant Time** | Takes the exact same time whether you have 10 items or 10,000,000 items! | Accessing a dictionary by key (`d["key"]`) or list by index (`lst[0]`) |
| **$O(\log N)$** | **Logarithmic Time** | Splitting a phone book in half repeatedly. Ultra fast. | Binary search, binary heap operations (`heapq.heappush`) |
| **$O(N)$** | **Linear Time** | Inspecting every single item one-by-one. Time doubles if data doubles. | Finding an item in an unsorted list (`val in my_list`) |
| **$O(N \log N)$** | **Log-Linear Time** | The standard speed of efficient sorting algorithms. | Python's `list.sort()` (Timsort) |
| **$O(N^2)$** | **Quadratic Time** | Comparing every item against every other item (nested loops). Dangerous for big data! | Nested `for` loops |

---

## 3. Lists vs. Tuples: Sequence Containers

### 1. Lists: Dynamic Arrays in Memory
A Python list is a **dynamic array** of contiguous pointers in RAM.
* **Indexing (`lst[i]`):** Instant $O(1)$ because memory offset is calculated mathematically: `address = base_address + (i * pointer_size)`.
* **Append (`lst.append(x)`):** Amortized $O(1)$ because Python **over-allocates** memory chunks (e.g. allocating space for 8 items when you add your 5th item).
* **Insert/Delete at Beginning (`lst.insert(0, x)` or `lst.pop(0)`):** Slow $O(N)$ because every existing element must be physically shifted in memory!

```python
# List Comprehension: Fast, pythonic way to transform lists
numbers = [1, 2, 3, 4, 5]
squares = [n ** 2 for n in numbers if n % 2 != 0]
print(squares)  # [1, 9, 25]
```

---

### 2. Tuples: Immutable Sequences
Tuples cannot be modified after creation (`immutability`).
* **Why use tuples?**
  1. **Memory efficiency:** Tuples have zero over-allocation overhead.
  2. **Data integrity:** Guarantees that values (e.g. `(latitude, longitude)`) cannot be accidentally mutated.
  3. **Hashable:** Tuples can be used as dictionary keys and set elements (if all contents are also immutable).

---

## 4. Dictionaries & Sets: The Hash Table Superpower

### How Dictionaries Work: The Hash Map Model
When you write `user["email"] = "alice@example.com"`:
1. Python runs `"email"` through a built-in mathematical algorithm called a **Hash Function**: `hash("email")` $\rightarrow$ `3829104821`.
2. Python uses this hash integer to instantly locate the exact memory bucket where the value is stored.
3. Lookup time is **$O(1)$ (Constant Time)** regardless of whether the dictionary has 5 keys or 5,000,000 keys!

```python
# The Key Immutability Rule:
# Dictionary keys MUST be hashable (immutable objects like str, int, float, tuple).
# You CANNOT use a mutable list as a dictionary key!
valid_dict = {("x", "y"): 100}  # ✅ Tuple key is valid
# invalid_dict = {["x", "y"]: 100} # ❌ TypeError: unhashable type: 'list'
```

---

### Sets: Fast Uniqueness & Mathematical Algebra
Sets are hash tables that only store unique keys without associated values:

```python
frontend_devs = {"Alice", "Bob", "Charlie"}
backend_devs = {"Charlie", "Diana", "Eve"}

# 1. Intersection (Who knows BOTH?): &
print(frontend_devs & backend_devs)  # {'Charlie'}

# 2. Union (All unique developers): |
print(frontend_devs | backend_devs)  # {'Alice', 'Bob', 'Charlie', 'Diana', 'Eve'}

# 3. Difference (Frontend ONLY): -
print(frontend_devs - backend_devs)  # {'Alice', 'Bob'}
```

---

## 5. The Specialized `collections` Module

Python's standard `collections` module provides optimized data structures for production engineering:

### 1. `deque` (Double-Ended Queue / Fast FIFO)
* Standard lists have $O(N)$ cost when popping from the front (`lst.pop(0)`).
* `collections.deque` provides **$O(1)$ instant appends and pops from BOTH ends**!

```python
from collections import deque

queue = deque(["Task 1", "Task 2"])
queue.append("Task 3")       # Add to right end in O(1)
first = queue.popleft()       # Remove from left end in O(1)!
print(f"Processed: {first}, Remaining: {list(queue)}")
```

---

### 2. `Counter` (Frequency Tracker)
Instantly counts occurrences in any sequence:

```python
from collections import Counter

votes = ["Alice", "Bob", "Alice", "Charlie", "Alice", "Bob"]
tally = Counter(votes)
print(tally)                   # Counter({'Alice': 3, 'Bob': 2, 'Charlie': 1})
print(tally.most_common(1))    # [('Alice', 3)]
```

---

### 3. `defaultdict` (No More `KeyError`)
Automatically initializes missing keys with a default factory (e.g. `list`, `int`, `set`):

```python
from collections import defaultdict

# Grouping students by grade without checking 'if grade in d:'
student_grades = defaultdict(list)
student_grades["A"].append("Alice")
student_grades["A"].append("Bob")
student_grades["B"].append("Charlie")

print(dict(student_grades))  # {'A': ['Alice', 'Bob'], 'B': ['Charlie']}
```

---

## 6. Priority Queues with `heapq` (Min-Heaps)

In a standard queue (FIFO), the first person in line is served first.
In a **Priority Queue**, the item with the **highest priority (or lowest numerical cost)** is always served first!

* `heapq` maintains a binary min-heap where the smallest item is always at index `0`:
* Insertion (`heappush`): $O(\log N)$
* Extraction (`heappop`): $O(\log N)$

```python
import heapq

# Priority queue of tasks: (priority_score, task_name)
task_queue = []
heapq.heappush(task_queue, (3, "Low priority cleanup"))
heapq.heappush(task_queue, (1, "CRITICAL SERVER OUTAGE"))
heapq.heappush(task_queue, (2, "Moderate bug fix"))

# Always pops the lowest priority number (highest urgency) first!
priority, task = heapq.heappop(task_queue)
print(f"Urgent Action: [{priority}] {task}")
# Output: Urgent Action: [1] CRITICAL SERVER OUTAGE
```

---

## 7. Data Structure Selection Cheat Sheet

| Use Case | Best Data Structure | Why |
| :--- | :--- | :--- |
| Ordered sequence with random index lookups | **`list`** | $O(1)$ index access, easy slicing |
| Fixed, immutable records | **`tuple`** | Low memory footprint, safe from mutation |
| Fast key-value lookups by unique name | **`dict`** | $O(1)$ lookups, insertions, and deletions |
| Unique elements, membership checks, set algebra | **`set`** | $O(1)$ `in` checks, eliminates duplicates |
| High-speed FIFO queues (Order books, task buffers) | **`collections.deque`** | $O(1)$ `append()` and $O(1)$ `popleft()` |
| Frequency counting and leaderboards | **`collections.Counter`** | Built-in multiset arithmetic and `most_common()` |
| Dynamic grouping of lists/sets by key | **`collections.defaultdict`** | Eliminates manual `if key not in dict:` boilerplate |
| Priority scheduling / limit price matching | **`heapq`** | $O(\log N)$ extraction of highest priority / lowest price |

---

## 8. Next Steps in this Module

1. **Interactive Notebook:** Open `05_interactive_data_structures.ipynb` to run live hash and heap benchmarks.
2. **Run Demonstrations:** Execute `06_lists_and_tuples_internals_demo.py`, `07_dicts_and_sets_hash_demo.py`, and `08_collections_and_heapq_demo.py`.
3. **Review Traps:** Check `09_TROUBLESHOOTING_AND_EDGE_CASES.md` (shallow vs deep copy, mutable dict keys).
4. **Self-Assessment:** Complete the quiz in `10_SELF_ASSESSMENT_AND_CHALLENGES.md`.
5. **Build the Mini-Project:** Follow `11_PROJECT_GUIDE.md` to explore the **High-Frequency Order Matching Engine** in `project_solution/`!
