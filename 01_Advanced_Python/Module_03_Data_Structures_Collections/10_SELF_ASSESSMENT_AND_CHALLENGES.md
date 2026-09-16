# Module 03: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Python data structures, time complexity, hash tables, and specialized collections before moving to **Module 04**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Time Complexity:** Why is accessing a list element by index (`lst[500]`) an $O(1)$ constant time operation, while finding an element by value (`500 in lst`) is $O(N)$ linear time?
2. **List Internals:** Why does Python over-allocate memory when growing a list with `append()`, rather than allocating exact space for one item at a time?
3. **Immutability & Hashing:** Why does Python raise a `TypeError` if you try to use a list as a dictionary key, but allows tuples?
4. **Queue Performance:** If you need a FIFO (First-In, First-Out) queue that processes 1,000,000 items, why should you use `collections.deque` instead of a standard `list`?
5. **Dictionary Merging:** What is the syntax for merging two dictionaries `a` and `b` in Python 3.9+ using the union operator, and which dictionary takes precedence in key conflicts?
6. **Set Algebra:** If `set_a = {1, 2, 3}` and `set_b = {3, 4, 5}`, what are the results of `set_a & set_b`, `set_a | set_b`, and `set_a - set_b`?
7. **`defaultdict` Behavior:** What happens when you access a key that does not exist in a `defaultdict(list)`?
8. **Heap Queues:** What is the time complexity of pushing an item onto a heap (`heapq.heappush`) and popping the smallest item (`heapq.heappop`)?
9. **Copy Semantics:** What is the difference between a shallow copy (`list.copy()`) and a deep copy (`copy.deepcopy()`) when dealing with nested lists?
10. **Encapsulation:** How can you expose an internal dictionary as read-only to external callers without copying the entire dictionary?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- A list is stored in contiguous RAM. Accessing by index uses pointer arithmetic: `address = base + (index * 8 bytes)`, which computes immediately in **$O(1)$**.
- Finding by value requires scanning every element sequentially from index $0$ to $N-1$, taking **$O(N)$** linear time.

#### Answer 2:
Over-allocating memory ensures that most `append()` operations simply write to already-reserved memory without needing expensive operating system memory reallocations, giving `append()` an **amortized $O(1)$** running time.

#### Answer 3:
Dictionary keys must be **hashable** (their hash value must never change over their lifetime). Lists are mutable (elements can be added/removed, changing their identity), whereas tuples are immutable.

#### Answer 4:
`list.pop(0)` takes $O(N)$ time because removing the first element requires shifting all remaining elements to the left. `collections.deque` is a doubly-linked list of memory blocks providing **$O(1)$ instant pops from both ends**.

#### Answer 5:
The syntax is `merged = a | b`. In case of duplicate keys, the right-hand dictionary (`b`) overrides the values from the left-hand dictionary (`a`).

#### Answer 6:
- `set_a & set_b` (Intersection): `{3}`
- `set_a | set_b` (Union): `{1, 2, 3, 4, 5}`
- `set_a - set_b` (Difference): `{1, 2}`

#### Answer 7:
It calls the factory function (here `list()`) to create an empty list `[]`, inserts it under the requested key, and returns the newly created list without raising a `KeyError`.

#### Answer 8:
Both operations run in **$O(\log N)$ logarithmic time**, where $N$ is the number of elements in the binary heap.

#### Answer 9:
- A **shallow copy** duplicates the outer container, but child/nested objects inside still point to the same memory references.
- A **deep copy** recursively duplicates every single nested container and object, creating a 100% isolated clone.

#### Answer 10:
Wrap the dictionary with **`types.MappingProxyType(internal_dict)`**. It provides a read-only view that prevents mutations without duplicating memory.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Anagram Grouping with `defaultdict`

**Goal:** Write a function `group_anagrams(words: list[str]) -> list[list[str]]` that groups words that are anagrams of each other (e.g. `"eat"`, `"tea"`, `"ate"`).

**Requirements:**
1. Use `collections.defaultdict` for optimal $O(N \cdot K \log K)$ performance.
2. Return a list of grouped word lists.

<details>
<summary><b>Solution Code</b></summary>

```python
from collections import defaultdict

def group_anagrams(words: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for word in words:
        # Canonical signature: sorted tuple of characters
        signature = tuple(sorted(word.lower()))
        groups[signature].append(word)
    return list(groups.values())

# Verification:
input_words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print("Grouped Anagrams:", group_anagrams(input_words))
# Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```
</details>

---

### Challenge 2: LRU (Least Recently Used) Cache

**Goal:** Implement a simple `LRUCache` class using `collections.OrderedDict` with a fixed `capacity`.
When capacity is exceeded, the least recently accessed key must be evicted.

<details>
<summary><b>Solution Code</b></summary>

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[str, int] = OrderedDict()

    def get(self, key: str) -> int | None:
        if key not in self.cache:
            return None
        # Move key to end to mark as recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Evict oldest (least recently used) item from front
            self.cache.popitem(last=False)

# Verification:
lru = LRUCache(2)
lru.put("A", 1)
lru.put("B", 2)
print(lru.get("A"))  # 1 (A becomes most recent)
lru.put("C", 3)      # Evicts B!
print(lru.get("B"))  # None (B was evicted)
print(lru.get("C"))  # 3
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Shallow copy of nested data

```python
template = {"tags": [], "meta": {"v": 1}}
a = template.copy()
b = template.copy()
a["tags"].append("x")
print(b["tags"])
```

**Observed symptom:** Prints `['x']` — the two copies share their inner list.

**(a)** What exactly did `.copy()` duplicate?

**(b)** What are the two correct approaches?

**(c)** Why is `deepcopy` not always the right answer?

<details>
<summary><b>Show the diagnosis</b></summary>

`.copy()` is **shallow**: it creates a new outer dict whose values are the *same objects*. Both copies hold a reference to one list.

**Two approaches:** `copy.deepcopy(template)` recursively duplicates everything; or restructure so there is nothing to share — build a fresh dict per use, or make the template immutable (`"tags": ()`) so mutation is impossible.

**`deepcopy` is not always right** because it is slow (it walks the whole graph and maintains a memo table for cycles), it copies things you may want shared (an open connection, a logger, a lock), and it fails on objects that are not copyable. Prefer designing the sharing away: a factory function or `field(default_factory=...)` beats copying after the fact.

</details>

---

### D2. Mutating a dict during iteration

```python
counts = {"a": 0, "b": 3, "c": 0, "d": 5}
for key in counts:
    if counts[key] == 0:
        del counts[key]
```

**Observed symptom:** `RuntimeError: dictionary changed size during iteration`.

**(a)** Why does Python refuse this rather than coping?

**(b)** What are the two standard fixes?

**(c)** Does the same restriction apply to lists?

<details>
<summary><b>Show the diagnosis</b></summary>

The iterator holds a position into the dict's internal table. Deleting an entry can trigger a resize and rehash, which would make that position meaningless — the iterator could skip entries or return them twice. Python detects the size change and raises rather than yielding silently wrong results.

**Two fixes:** iterate over a snapshot — `for key in list(counts):` — or build a new dict, which is cleaner: `counts = {k: v for k, v in counts.items() if v != 0}`.

**Lists are worse:** mutating a list during iteration does **not** raise. It silently skips elements, because the index advances while the list shrinks. `for x in xs: if bad(x): xs.remove(x)` quietly leaves bad items behind. A raised error is a gift; the list version is the genuinely dangerous one.

</details>

---

### D3. Unhashable key

```python
index: dict[list[str], int] = {}
index[["a", "b"]] = 1
```

**Observed symptom:** `TypeError: unhashable type: 'list'`.

**(a)** Why can a list not be a dict key?

**(b)** What should you use instead?

**(c)** What makes a custom class usable as a key?

<details>
<summary><b>Show the diagnosis</b></summary>

A dict places a key in a bucket derived from its hash. If the key were mutable, changing it after insertion would change its hash, and the entry would become unfindable — present in the dict but unreachable. Python forbids the situation by making mutable builtins unhashable.

**Use instead:** a `tuple` (`("a", "b")`) for an ordered key, or `frozenset` when order should not matter.

**A custom class** is hashable by default (identity-based), and stays valid as long as you do not define `__eq__`. If you do define `__eq__`, you must define a consistent `__hash__` over the *immutable* parts — or use `@dataclass(frozen=True)`, which generates both. Module 04's diagnostic D2 covers what goes wrong when they disagree.

</details>

---

### D4. defaultdict creates entries on read

```python
from collections import defaultdict

scores = defaultdict(int)
scores["ada"] = 10

if scores["bob"] > 5:
    print("bob qualifies")

print(len(scores), dict(scores))
```

**Observed symptom:** Prints `2 {'ada': 10, 'bob': 0}` — merely checking `bob` created the key.

**(a)** Why did a read insert a key?

**(b)** How do you check membership without inserting?

**(c)** When does this cause a real bug rather than a curiosity?

<details>
<summary><b>Show the diagnosis</b></summary>

`defaultdict.__missing__` is called on a failed lookup and it **inserts** the default before returning it. Any `d[key]` on a `defaultdict` is potentially a write.

**Check without inserting:** `scores.get("bob", 0)` or `if "bob" in scores`. Neither goes through `__missing__`.

**Real bugs:** iterating a `defaultdict` while reading unknown keys mutates it mid-iteration (see D2 above); serialising it to JSON emits phantom entries that a consumer treats as real data; and a memory leak in a long-lived process that probes many never-present keys. The behaviour is correct and documented — the mistake is reaching for `defaultdict` when you only wanted a default *value*, where `.get()` is the right tool.

</details>

---

### D5. Wrong container for the access pattern

```python
seen: list[str] = []
for record in records:          # 100,000 records
    if record["id"] not in seen:
        seen.append(record["id"])
```

**Observed symptom:** Correct output; takes 40 seconds and gets quadratically worse.

**(a)** What is the complexity of `in` on a list versus a set?

**(b)** What is the rewrite?

**(c)** When is a list genuinely the right choice for membership testing?

<details>
<summary><b>Show the diagnosis</b></summary>

`x in list` is **O(n)** — a linear scan. Inside a loop over n records that is O(n²): 100,000 records means up to 5 billion comparisons.

**Rewrite:** `seen: set[str] = set()` with `seen.add(...)`. Set membership is O(1) average, making the loop O(n) — the 40 seconds becomes milliseconds. If insertion order matters, `dict.fromkeys()` preserves it while keeping O(1) lookups.

**A list is right** when it is tiny (under roughly 10 elements, where the constant factors favour a scan and hashing costs more than it saves), when the elements are unhashable, or when you need the sequence for something else anyway and membership is a rare operation. Choosing the container from the access pattern rather than from habit is the whole lesson of this module.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
