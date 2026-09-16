# The Pattern Recognition Guide — How To Attack A Problem You Have Never Seen

> Knowing how a heap works does not tell you that "k-th largest" means heap.
> This guide is the missing half of the course: a **decision procedure** you run
> on an unseen problem to decide what to build.
>
> Everything here is drilled in the per-module `problems/` directories. Read this
> once now, then re-read the triage section every time you get stuck.

---

## Part 0 — Why most people plateau

They learn fifteen data structures and still freeze on a new problem, because
they practised *implementations* and the interview asks for a *diagnosis*.

The fix is to make the diagnosis mechanical. There are roughly twenty patterns
in the whole subject. Almost every problem you will meet is one of them, or two
of them composed. Your job in the first two minutes is not to solve the problem —
it is to **name the pattern**.

---

## Part 1 — The 60-second triage

Run these five steps, in order, before writing anything.

### Step 1: Read the constraints first, not the story

The constraint on `n` tells you the complexity you are allowed, and the
complexity tells you the technique. This is the single highest-leverage habit in
competitive and interview programming, and most people skip it.

| Constraint on `n` | Budget you can afford | Techniques that fit |
| :--- | :--- | :--- |
| `n ≤ 10` | `O(n!)`, `O(n·n!)` | Backtracking over all permutations |
| `n ≤ 20` | `O(2ⁿ)`, `O(2ⁿ·n)` | Subset enumeration, **bitmask DP** |
| `n ≤ 100` | `O(n⁴)` | 3-nested loops plus work, Floyd-Warshall on small graphs |
| `n ≤ 500` | `O(n³)` | Floyd-Warshall, interval DP (`dp[i][j]` with a split loop) |
| `n ≤ 5·10³` | `O(n²)` | 2D DP, all-pairs on sequences, LCS / edit distance |
| `n ≤ 10⁵` | `O(n log n)` | Sort, heap, binary search, segment tree, Dijkstra |
| `n ≤ 10⁶` | `O(n)` | Hash map, two pointers, sliding window, prefix sums, linear DP |
| `n ≤ 10⁹` | `O(log n)` or `O(√n)` | **Binary search on the answer**, math, fast exponentiation |
| `n` is astronomically large | `O(1)` | Closed-form formula, matrix exponentiation |

**How to use it:** a problem with `n ≤ 10⁵` and an obvious `O(n²)` brute force is
telling you, explicitly, that an `O(n log n)` or `O(n)` method exists. The
constraint is a hint, not a hurdle.

The reverse is just as useful. `n ≤ 20` with a "find the best arrangement"
question is almost always bitmask DP — nothing else has that shape.

### Step 2: Name the output shape

| The problem asks for | That usually means |
| :--- | :--- |
| A single number (max/min/count) | DP, greedy, or a math identity |
| "Does there exist…" (yes/no) | Search, DP reachability, or union-find |
| **All** valid configurations | Backtracking — the output size forces exponential |
| The k-th / top-k something | Heap, quickselect, or binary search on value |
| A contiguous run | Sliding window or prefix sums |
| A pair or triple satisfying a relation | Sorting + two pointers, or a hash map |
| An ordering subject to prerequisites | Topological sort |
| A shortest / cheapest path | BFS (unweighted), Dijkstra (non-negative), Bellman-Ford (negative) |
| Something about prefixes of strings | Trie |
| Connectivity / grouping | Union-find or DFS flood fill |

Asking for *all* solutions rules out DP immediately: DP compresses the state
space, which is exactly what destroys the individual answers.

### Step 3: Look for the structural giveaway

| If the input has this property | Reach for |
| :--- | :--- |
| **Sorted** (or you may sort it) | Binary search, two pointers |
| Sorted and you need a pair summing to `X` | Two pointers from both ends — `O(n)`, no hash map needed |
| A monotonic predicate over the answer | Binary search on the answer |
| Overlapping subproblems + optimal substructure | DP |
| A locally-best choice that is provably globally safe | Greedy — **and you must prove it** |
| Nested / balanced structure | Stack |
| "Next greater / previous smaller" | **Monotonic stack** |
| A window whose validity is monotone in its width | Sliding window |
| Intervals | Sort by start (merging) or by end (scheduling) |
| A grid | BFS / DFS / DP over `(row, col)` |
| Repeated range queries with updates | Segment tree or Fenwick tree |
| Repeated range queries, no updates | Prefix sums |

### Step 4: State the brute force out loud, then find what it repeats

Every efficient algorithm is a brute force with a repetition removed. Naming
the repetition names the technique:

| The brute force repeats… | Removed by |
| :--- | :--- |
| The same subproblem | Memoization → DP |
| A scan over a window that mostly did not change | Sliding window |
| A search over a sorted region | Binary search |
| A recomputation of a range sum | Prefix sums |
| A comparison against the current best-so-far | Monotonic stack / heap |
| A traversal from every start node | Multi-source BFS, or precomputation |

This step is also what you say in an interview. "The brute force is `O(n²)`
because I re-scan the window each time; the window only changes by one element,
so I can maintain it in `O(1)` and get `O(n)`" is a complete, senior-sounding
answer.

### Step 5: Commit, and set a budget

Pick the pattern, say it out loud, and give yourself a time budget (10 minutes
of practice time, 5 in an interview). If the approach has not started working by
then, go back to Step 3 — do not keep pushing a wrong pattern. Most failed
attempts are a correct implementation of the wrong idea.

---

## Part 2 — Signal → pattern lookup

Keyword and phrase triggers. Not infallible, but a fast first guess.

| Words in the problem | First guess |
| :--- | :--- |
| "contiguous", "subarray", "substring" | Sliding window / prefix sums |
| "longest substring with at most k…" | Variable-size sliding window |
| "exactly k distinct" | Sliding window, computed as `atMost(k) − atMost(k−1)` |
| "subsequence" (not contiguous) | DP |
| "palindrome" | Two pointers, or interval DP |
| "anagram" | Character counts in a hash map |
| "next greater", "next smaller", "span" | Monotonic stack |
| "sliding window maximum" | Monotonic **deque** |
| "k-th largest / smallest" | Heap of size k, or quickselect |
| "median of a stream" | Two heaps |
| "merge k sorted…" | Min-heap of k pointers |
| "top k frequent" | Counter + heap, or bucket sort |
| "minimum number of steps / moves" (unweighted) | **BFS** — not DFS |
| "shortest path", weights ≥ 0 | Dijkstra |
| "shortest path", negative weights | Bellman-Ford |
| "can finish all courses", "build order" | Topological sort |
| "number of islands / regions / provinces" | DFS flood fill or union-find |
| "connected", "same group", "redundant connection" | Union-find |
| "cycle" in a directed graph | DFS with three colours |
| "cycle" in a linked list | Floyd's fast/slow pointers |
| "generate all", "enumerate every" | Backtracking |
| "N-queens", "sudoku", "word search" | Backtracking with pruning |
| "minimum coins", "ways to make change" | DP (unbounded knapsack) |
| "can partition into equal sum" | DP (0/1 knapsack, subset-sum) |
| "edit distance", "common subsequence" | 2D DP |
| "buy and sell stock" | DP with a state machine, or greedy |
| "minimum rooms / platforms / arrows" | Greedy on sorted intervals |
| "merge overlapping intervals" | Sort by start, then sweep |
| "maximum non-overlapping intervals" | Sort by **end**, then greedy |
| "prefix", "autocomplete", "starts with" | Trie |
| "range sum with updates" | Segment tree / Fenwick |
| "minimise the maximum", "maximise the minimum" | **Binary search on the answer** |
| "capacity to ship in D days", "koko eating bananas" | Binary search on the answer |
| "n ≤ 20" plus "best arrangement" | Bitmask DP |
| "in-place", "O(1) extra space" | Two pointers, or index encoding |
| "detect duplicate in O(1) space" | Cycle detection on the value graph |

---

## Part 3 — The twenty patterns

Each entry: **when it applies**, the **template**, and **how it fails** — because
knowing the failure mode is what stops you misapplying it.

### 1. Two pointers (opposite ends)

**Applies when** the array is sorted and you need a pair/triple with a target
relation. Moving a pointer must monotonically change the objective.

```python
lo, hi = 0, len(a) - 1
while lo < hi:
    s = a[lo] + a[hi]
    if s == target:
        return lo, hi
    if s < target:
        lo += 1          # only way to increase the sum
    else:
        hi -= 1          # only way to decrease it
```

**Fails when** the array is unsorted and sorting destroys required index
information — then use a hash map instead.

### 2. Two pointers (same direction / fast-slow)

**Applies when** removing/partitioning in place, or detecting a cycle.

```python
write = 0
for read in range(len(a)):
    if keep(a[read]):
        a[write] = a[read]
        write += 1
return write        # new logical length
```

**Fails when** order must be preserved *and* you need stability with extra
constraints — check whether an auxiliary array is actually allowed.

### 3. Sliding window (fixed size)

**Applies when** you need something about every window of size `k`.

```python
total = sum(a[:k])
best = total
for i in range(k, len(a)):
    total += a[i] - a[i - k]     # the whole trick: O(1) update
    best = max(best, total)
```

### 4. Sliding window (variable size)

**Applies when** the window's validity is **monotone**: growing it can only make
it worse, shrinking can only make it better.

```python
left = 0
best = 0
state = {}
for right, x in enumerate(a):
    add(state, x)
    while not valid(state):       # shrink until valid again
        remove(state, a[left])
        left += 1
    best = max(best, right - left + 1)
```

**Fails when** validity is not monotone — e.g. "sum exactly k" with negative
numbers. A window can become valid again after growing, so shrinking is wrong.
Use prefix sums with a hash map instead.

### 5. Prefix sums / difference arrays

**Applies when** you need many range sums with no updates, or many range
*updates* with one final read.

```python
pre = [0]
for x in a:
    pre.append(pre[-1] + x)
range_sum = pre[j + 1] - pre[i]        # inclusive i..j
```

For subarray-sum-equals-k with negatives, pair it with a hash map of
prefix-count — this is the canonical case where sliding window fails and prefix
sums succeed.

### 6. Binary search (on an index)

**Applies when** the array is sorted. Use the half-open invariant to avoid
off-by-one bugs forever:

```python
lo, hi = 0, len(a)                 # hi is EXCLUSIVE
while lo < hi:
    mid = (lo + hi) // 2
    if a[mid] < target:
        lo = mid + 1
    else:
        hi = mid
return lo                          # first index with a[i] >= target
```

**Fails when** the predicate is not monotone. Binary search needs
`False…False True…True`, nothing else.

### 7. Binary search on the answer

**Applies when** you cannot compute the answer directly, but you *can* cheaply
check "is `x` achievable?", and achievability is monotone in `x`. This is the
most under-recognised pattern in the whole subject.

```python
def feasible(x) -> bool: ...        # monotone in x

lo, hi = min_possible, max_possible
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        hi = mid                    # minimising
    else:
        lo = mid + 1
return lo
```

**Recognition cue:** "minimise the maximum", "maximise the minimum", "smallest
capacity such that…", "least speed such that…", plus a huge value range and a
small `n`.

### 8. Monotonic stack

**Applies when** you need the next/previous greater/smaller element, or the
largest rectangle under a histogram.

```python
stack = []                          # holds indices, values increasing
result = [-1] * len(a)
for i, x in enumerate(a):
    while stack and a[stack[-1]] < x:
        result[stack.pop()] = i     # x is the next greater for that index
    stack.append(i)
```

**Why it is `O(n)`:** each index is pushed once and popped at most once. Say
that out loud in an interview; the `while` inside a `for` makes it look `O(n²)`.

### 9. Monotonic deque

**Applies when** you need the max/min of a *sliding* window in `O(n)`.

```python
from collections import deque
dq = deque()                        # indices, values decreasing
for i, x in enumerate(a):
    while dq and a[dq[-1]] <= x:
        dq.pop()                    # dominated: newer AND bigger
    dq.append(i)
    if dq[0] <= i - k:
        dq.popleft()                # left the window
    if i >= k - 1:
        out.append(a[dq[0]])
```

### 10. Hash map for complements and counting

**Applies when** you need `O(1)` lookup of "have I seen X?" — pair sums,
anagrams, frequency, deduplication, prefix-sum counts.

**Fails when** you need *order* or *range* queries. A hash map has neither.

### 11. Heap / priority queue

**Applies when** you repeatedly need the current extreme of a changing
multiset: top-k, k-way merge, streaming median (two heaps), scheduling.

**The size-k trick:** for k-th largest, keep a **min**-heap of size k. The root
is the answer, and it costs `O(n log k)` rather than `O(n log n)`.

### 12. Sorting as a preprocessing step

**Applies when** sorting exposes structure: intervals, two pointers, greedy
ordering, deduplication. `O(n log n)` is usually free relative to the rest.

**The key decision for intervals:** sort by **start** to merge, sort by **end**
to schedule the maximum number of non-overlapping items. Getting this backwards
produces a plausible wrong answer, not an error.

### 13. BFS

**Applies when** you need the shortest path in an **unweighted** graph, or level
order. BFS's first arrival at a node is optimal; DFS's is not.

```python
from collections import deque
q = deque([start])
dist = {start: 0}
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in dist:           # mark on ENQUEUE, not on dequeue
            dist[v] = dist[u] + 1
            q.append(v)
```

**The classic bug:** marking visited when you *dequeue* instead of when you
*enqueue*. Nodes then get queued many times; the answer is still right but the
complexity degrades badly, and on a large grid it looks like a hang.

**Multi-source BFS:** seed the queue with every source at distance 0. This turns
"nearest X for every cell" from `O(V·E)` into one `O(V+E)` pass.

### 14. DFS

**Applies when** you need reachability, connected components, cycle detection,
or a topological order. Use an explicit stack when recursion depth could exceed
~10⁴ — Python's default limit is 1000.

**Directed cycle detection needs three states**, not two:

```python
WHITE, GREY, BLACK = 0, 1, 2        # unvisited, on stack, done
def dfs(u):
    colour[u] = GREY
    for v in adj[u]:
        if colour[v] == GREY:
            return True             # back edge -> cycle
        if colour[v] == WHITE and dfs(v):
            return True
    colour[u] = BLACK
    return False
```

With only visited/unvisited you report a cycle for any re-encountered node,
including a diamond — a false positive on a perfectly valid DAG.

### 15. Topological sort

**Applies when** there are prerequisites. Kahn's algorithm doubles as cycle
detection: if the output is shorter than `V`, a cycle exists.

### 16. Union-find (disjoint set union)

**Applies when** you merge groups and ask "same group?" — connectivity,
Kruskal's MST, redundant edges, accounts merge.

Path compression + union by rank gives near-`O(1)` amortised. **Union-find
cannot delete edges** — if the problem removes connections, you need a different
approach (often: process in reverse).

### 17. Dynamic programming

**Applies when** there are overlapping subproblems and optimal substructure.
Four questions, in this order:

1. **What is the state?** The minimal information identifying a subproblem.
2. **What is the transition?** How states combine.
3. **What is the base case?**
4. **What is the order?** Every state must be computed before it is used.

Write it top-down with memoisation first — the recursion mirrors the transition
and is far easier to get right. Convert to bottom-up only if you need the
constant factor or the space saving.

**Rolling-array space reduction:** if `dp[i]` depends only on `dp[i-1]`, keep two
rows and go from `O(n·m)` to `O(m)`.

### 18. Greedy

**Applies when** a locally optimal choice is provably globally optimal. The
proof is not optional — greedy is the pattern people get wrong most often,
because a wrong greedy passes the examples and fails on a case you did not think
of.

**Two standard proofs:** the *exchange argument* (any optimal solution can be
transformed into the greedy one without getting worse) and the *staying-ahead
argument* (greedy's partial solution is never behind).

**If you cannot prove it, use DP.** DP is slower and always correct.

### 19. Backtracking

**Applies when** you must enumerate all valid configurations.

```python
def backtrack(path, choices):
    if is_solution(path):
        out.append(path[:])         # COPY - path is mutated after this
        return
    for c in choices:
        if not promising(path, c):
            continue                # pruning is where the speed lives
        path.append(c)
        backtrack(path, remaining(choices, c))
        path.pop()                  # undo
```

**Two classic bugs:** appending `path` instead of `path[:]` (every result ends
up the same mutated list), and forgetting the `pop()`.

**Duplicate handling:** sort the input, then skip `i > start and a[i] == a[i-1]`.

### 20. Bit manipulation and bitmask DP

**Applies when** `n ≤ 20` and the state is "which subset have I used". A mask is
an integer; `dp[mask]` is the answer for that subset.

Useful identities: `x & (x-1)` clears the lowest set bit; `x & -x` isolates it;
`bin(x).count("1")` is the popcount; `mask | (1 << i)` adds element `i`.

---

## Part 4 — Worked triage

### Example A

> Given an array of `n ≤ 10⁵` integers and an integer `k`, find the maximum sum
> of any contiguous subarray of length exactly `k`.

- **Step 1:** `n ≤ 10⁵` → `O(n log n)` or better. `O(n·k)` brute force is too slow.
- **Step 2:** output is a single number → DP, greedy, or a scan.
- **Step 3:** "contiguous" + fixed length → fixed-size sliding window.
- **Step 4:** brute force re-sums each window; consecutive windows share `k−1`
  elements. That is the repetition.
- **Verdict:** fixed sliding window, `O(n)` time, `O(1)` space.

### Example B

> `n ≤ 10⁵` packages with weights. Ship all of them within `D` days, shipping in
> order. Find the minimum ship capacity.

- **Step 1:** `n ≤ 10⁵`, but the *answer* ranges up to `sum(weights)` ≈ 10⁹.
- **Step 2:** "minimum capacity such that…" → minimise subject to feasibility.
- **Step 3:** is feasibility monotone in capacity? A bigger ship can always do
  what a smaller one could. **Yes** → binary search on the answer.
- **Step 4:** `feasible(cap)` is a single greedy `O(n)` pass.
- **Verdict:** binary search on the answer, `O(n log(sum))`.

Note that no data structure appears at all. The pattern *was* the answer.

### Example C

> Given `n ≤ 20` cities and a distance matrix, find the shortest tour visiting
> every city once.

- **Step 1:** `n ≤ 20` → `O(2ⁿ·n²)` ≈ 4·10⁸ is the intended budget. `n!` is not.
- **Step 2:** single number, "visit every one" → subset state.
- **Step 3:** `n ≤ 20` + optimal arrangement → **bitmask DP**.
- **Verdict:** `dp[mask][last]`, Held-Karp, `O(2ⁿ·n²)`.

The constraint alone identified this. Nothing in the wording said "DP".

---

## Part 5 — When you are stuck

Work down this ladder. Do not skip.

1. **Re-read the constraints.** Half of all stuck moments are a missed bound.
2. **Do a tiny case by hand** — `n = 1`, `n = 2`, `n = 3`. Patterns become
   visible at `n = 3` that are invisible in the abstract.
3. **Write the brute force.** A working slow solution beats a broken fast one,
   and it gives you something to optimise and to test against.
4. **Ask what the brute force repeats.** See Step 4 above.
5. **Try to sort the input.** Astonishingly often this is the whole insight.
6. **Ask what you would need to know to answer in `O(1)`,** then ask whether you
   can precompute it.
7. **Change the question.** Instead of "what is the answer", ask "given a
   candidate answer, can I verify it?" If verification is easy and monotone,
   binary search on the answer.
8. **Look for the inverse.** Counting the complement is sometimes far easier.
9. **Draw the state machine.** For anything with modes — buy/sell/cooldown —
   the states *are* the DP.
10. **Give up deliberately, read the solution, then re-derive it from scratch
    the next day.** Reading a solution teaches you nothing; re-deriving it
    teaches you everything. Put it on a 3-day re-attempt schedule.

---

## Part 6 — Verify before you claim

Habits that catch the bugs this course's debug labs are built from:

- **Test `n = 0` and `n = 1`.** Most off-by-one bugs surface immediately.
- **Test duplicates.** Two-pointer and backtracking dedup logic breaks here.
- **Test all-equal and already-sorted input.** Quicksort partitioning and
  monotonic stacks degrade or break.
- **Test negative numbers.** Sliding-window solutions that assume positivity
  fail silently — they return a plausible number.
- **Check integer overflow in `mid`.** `(lo + hi) // 2` is safe in Python but is
  a real bug in C++/Java; write `lo + (hi - lo) // 2` if you will port it.
- **Count your recursion depth.** Python's default limit is 1000; a linked list
  of 10⁵ nodes will blow it.
- **State your complexity out loud and check it against the constraint.** If
  they disagree, you have the wrong pattern — go back to Step 3.

---

## Where this is drilled

| Pattern | Module | Problem set |
| :--- | :--- | :--- |
| Two pointers, sliding window, prefix sums | [02](Module_02_Arrays_Dynamic_Arrays_and_Strings/01_README.md) | `problems/` |
| Fast/slow pointers, in-place reversal | [03](Module_03_Linked_Lists_and_Pointer_Manipulation/01_README.md) | `problems/` |
| Monotonic stack and deque | [04](Module_04_Stacks_Queues_and_Monotonic_Structures/01_README.md) | `problems/` |
| Hash map complements and counting | [05](Module_05_Hash_Tables_and_Collision_Resolution/01_README.md) | `problems/` |
| Tree traversal, BST invariants | [06](Module_06_Trees_Binary_Search_Trees_and_Self_Balancing/01_README.md) | `problems/` |
| Heaps, top-k, streaming median | [07](Module_07_Heaps_Priority_Queues_and_TopK_Patterns/01_README.md) | `problems/` |
| BFS, DFS, topological sort | [08](Module_08_Graph_Algorithms_Traversals_and_DAGs/01_README.md) | `problems/` |
| Dijkstra, Bellman-Ford, MST | [09](Module_09_Graph_Algorithms_Shortest_Paths_and_MST/01_README.md) | `problems/` |
| 1D DP, sequences, state machines | [10](Module_10_Dynamic_Programming_1D_and_Sequence_Patterns/01_README.md) | `problems/` |
| 2D DP, knapsack, grids | [11](Module_11_Dynamic_Programming_2D_Knapsack_and_Grids/01_README.md) | `problems/` |
| Greedy, intervals | [12](Module_12_Greedy_Algorithms_and_Interval_Scheduling/01_README.md) | `problems/` |
| Backtracking, pruning | [13](Module_13_Backtracking_and_Constraint_Satisfaction/01_README.md) | `problems/` |
| Trie, union-find, segment tree | [14](Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/01_README.md) | `problems/` |
| Binary search on the answer | [02](Module_02_Arrays_Dynamic_Arrays_and_Strings/01_README.md), [12](Module_12_Greedy_Algorithms_and_Interval_Scheduling/01_README.md) | `problems/` |

---

[Course README](README.md) · [Master Syllabus](MASTER_SYLLABUS.md) · [Roadmap](ROADMAP_DSA_MASTER.md)
