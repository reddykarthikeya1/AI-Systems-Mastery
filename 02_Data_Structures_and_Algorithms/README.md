# 02. Data Structures & Algorithms — 0 to 100 Mastery

Welcome to **Data Structures & Algorithms (DSA)**, engineered from first principles for dual-threat mastery: acing rigorous FAANG/Top-Tech algorithmic interviews and writing high-performance, cache-conscious systems code.

---

## Pedagogical Philosophy: From Intuition to Hardware Reality

Most DSA courses teach code in a vacuum without explaining memory layout, pointer indirection, or hardware bottlenecks. This curriculum connects mathematical complexity directly to physical CPU cache lines, branch predictors, and production systems architectures:
- **Beginner-Friendly Onboarding**: Every abstract structure begins with visual ASCII memory maps and real-world analogies.
- **Strict Big-O Proofs**: Rigorous time, space, and amortized complexity bounds.
- **Production Systems Bridges**: Connects standard data structures to real distributed databases and AI engines (e.g., Skip Lists in RocksDB, Bloom Filters in Cassandra, Ring Buffers in Disruptor, Priority Queues in Ray schedulers).

---

## 15-Module Master Roadmap

| # | Module | Core Focus | Materials |
|---|---|---|---|
| **01** | [Complexity Analysis & Memory Layout](Module_01_Complexity_Analysis_and_Memory_Layout/01_README.md) | Big-O, Big-Omega, Amortized Analysis, CPU Cache Locality, and Branch Prediction | [Read](Module_01_Complexity_Analysis_and_Memory_Layout/01_README.md) · [Project](Module_01_Complexity_Analysis_and_Memory_Layout/04_PROJECT_GUIDE.md) |
| **02** | [Arrays, Dynamic Arrays & Strings](Module_02_Arrays_Dynamic_Arrays_and_Strings/01_README.md) | Memory Reallocation, Resizing Amortization, Two-Pointers, and Sliding Window | [Read](Module_02_Arrays_Dynamic_Arrays_and_Strings/01_README.md) · [Project](Module_02_Arrays_Dynamic_Arrays_and_Strings/07_PROJECT_GUIDE.md) |
| **03** | [Linked Lists & Node Structures](Module_03_Linked_Lists_and_Pointer_Manipulation/01_README.md) | Singly/Doubly Linked Lists, Fast & Slow Pointers, Cycle Detection, and Reverse Operations | [Read](Module_03_Linked_Lists_and_Pointer_Manipulation/01_README.md) · [Project](Module_03_Linked_Lists_and_Pointer_Manipulation/04_PROJECT_GUIDE.md) |
| **04** | [Stacks, Queues & Monotonic Structures](Module_04_Stacks_Queues_and_Monotonic_Structures/01_README.md) | LIFO/FIFO Internals, Monotonic Stacks, Deques, and Sliding Window Maximum | [Read](Module_04_Stacks_Queues_and_Monotonic_Structures/01_README.md) · [Project](Module_04_Stacks_Queues_and_Monotonic_Structures/04_PROJECT_GUIDE.md) |
| **05** | [Hash Tables & Collision Resolution](Module_05_Hash_Tables_and_Collision_Resolution/01_README.md) | Hash Functions, Separate Chaining, Open Addressing, Robin Hood Hashing, and CPython Dict Internals | [Read](Module_05_Hash_Tables_and_Collision_Resolution/01_README.md) · [Project](Module_05_Hash_Tables_and_Collision_Resolution/04_PROJECT_GUIDE.md) |
| **06** | [Trees, BSTs & Balancing](Module_06_Trees_Binary_Search_Trees_and_Self_Balancing/01_README.md) | Tree Traversals (In/Pre/Post/Level), LCA, BST Invariants, and AVL/Red-Black Balancing Intuitions | [Read](Module_06_Trees_Binary_Search_Trees_and_Self_Balancing/01_README.md) · [Project](Module_06_Trees_Binary_Search_Trees_and_Self_Balancing/04_PROJECT_GUIDE.md) |
| **07** | [Heaps & Priority Queues](Module_07_Heaps_Priority_Queues_and_TopK_Patterns/01_README.md) | Binary Heaps, Heapify in O(N), Median of Streaming Data, and K-Way Merging | [Read](Module_07_Heaps_Priority_Queues_and_TopK_Patterns/01_README.md) · [Project](Module_07_Heaps_Priority_Queues_and_TopK_Patterns/04_PROJECT_GUIDE.md) |
| **08** | [Graph Traversals & DAGs](Module_08_Graph_Algorithms_Traversals_and_DAGs/01_README.md) | Adjacency Representations, BFS, DFS, Topological Sorting, and Cycle Detection | [Read](Module_08_Graph_Algorithms_Traversals_and_DAGs/01_README.md) · [Project](Module_08_Graph_Algorithms_Traversals_and_DAGs/04_PROJECT_GUIDE.md) |
| **09** | [Shortest Paths & Minimum Spanning Trees](Module_09_Graph_Algorithms_Shortest_Paths_and_MST/01_README.md) | Dijkstra with Heaps, Bellman-Ford, A* Search, Kruskal with DSU, and Prim's Algorithm | [Read](Module_09_Graph_Algorithms_Shortest_Paths_and_MST/01_README.md) · [Project](Module_09_Graph_Algorithms_Shortest_Paths_and_MST/04_PROJECT_GUIDE.md) |
| **10** | [Dynamic Programming: 1D & Sequences](Module_10_Dynamic_Programming_1D_and_Sequence_Patterns/01_README.md) | Memoization vs Tabulation, State Space Transitions, Fibonacci to Longest Increasing Subsequence | [Read](Module_10_Dynamic_Programming_1D_and_Sequence_Patterns/01_README.md) · [Project](Module_10_Dynamic_Programming_1D_and_Sequence_Patterns/04_PROJECT_GUIDE.md) |
| **11** | [Dynamic Programming: 2D & Knapsack](Module_11_Dynamic_Programming_2D_Knapsack_and_Grids/01_README.md) | 0/1 Knapsack, Unbounded Knapsack, Edit Distance, Longest Common Subsequence, and Grid Paths | [Read](Module_11_Dynamic_Programming_2D_Knapsack_and_Grids/01_README.md) · [Project](Module_11_Dynamic_Programming_2D_Knapsack_and_Grids/04_PROJECT_GUIDE.md) |
| **12** | [Greedy Algorithms & Intervals](Module_12_Greedy_Algorithms_and_Interval_Scheduling/01_README.md) | Greedy Choice Property, Interval Merging, Fractional Knapsack, and Huffman Coding | [Read](Module_12_Greedy_Algorithms_and_Interval_Scheduling/01_README.md) · [Project](Module_12_Greedy_Algorithms_and_Interval_Scheduling/04_PROJECT_GUIDE.md) |
| **13** | [Backtracking & State Search](Module_13_Backtracking_and_Constraint_Satisfaction/01_README.md) | State Space Trees, N-Queens, Sudoku Solver, Subset Sum, and Pruning Optimizations | [Read](Module_13_Backtracking_and_Constraint_Satisfaction/01_README.md) · [Project](Module_13_Backtracking_and_Constraint_Satisfaction/04_PROJECT_GUIDE.md) |
| **14** | [Advanced Trees & Sets](Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/01_README.md) | Trie (Prefix Trees), Disjoint Set Union (Union-Find with Path Compression), and Segment Trees | [Read](Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/01_README.md) · [Project](Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/04_PROJECT_GUIDE.md) |
| **15** | [Systems Data Structures](Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU/01_README.md) | Skip Lists, Bloom Filters, HyperLogLog, Ring Buffers, and O(1) LRU/LFU Cache Eviction | [Read](Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU/01_README.md) · [Project](Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU/04_PROJECT_GUIDE.md) |

---

## Fast-Track Navigation
- **[Pattern Recognition Guide](PATTERN_RECOGNITION_GUIDE.md)** — how to attack a problem you have never seen. Read this first.
- [DSA Master Roadmap (NeetCode 150 & Striver A2Z)](ROADMAP_DSA_MASTER.md)
- [Master Syllabus](MASTER_SYLLABUS.md)
- [Beginner Onboarding Guide](START_HERE_BEGINNER_GUIDE.md)
- [Study Plans & Pacing](STUDY_PLANS_AND_PACING_GUIDE.md)
- [Phase Checkpoints](Phase_Checkpoints/PHASE_01_CHECKPOINT.md) — 7 gates across the curriculum

---

## How This Course Is Actually Used

Reading a module teaches recognition. It does not teach recall, and it teaches
diagnosis not at all. Each module therefore ships four things, and they are
meant to be worked in this order.

| | What it is | What it builds |
| :--- | :--- | :--- |
| **1. README** | The concepts, with memory layout and complexity proofs | Recognition |
| **2. `starter/`** | Stubs for the module project; the shipped tests are the spec | Construction |
| **3. `problems/`** | **130 problems** across the 17 modules, pattern-indexed, with a 3-step hint ladder | Recall |
| **4. `debug_lab/`** | Planted defects that **exit 0** and print plausible wrong answers | Diagnosis |

### The problem bank

```bash
cd Module_02_*/problems
python -m pytest tests -q            # your stubs - must FAIL before you start
python -m pytest tests -q -k p03     # just problem 3
```

118 problems, each with the statement, the constraints, a complexity target and
three hints to be read one at a time. Every reference solution in
`problems/solutions/` is cross-checked in its own test against a brute force, a
library function or a second implementation — so the answers are verified rather
than asserted.

### The grading loop

Running a module's shipped tests from `starter/` must **fail**. If it passes on
an untouched stub, the course is certifying work that was never done:

```bash
make integrity          # asserts this property across all 17 modules
```

That invariant is checked rather than assumed, because this course shipped with
it broken.

### Verification

```bash
make verify             # lint, links, deps, tests, integrity - fail-fast
make test               # 204 tests: module projects + problem bank
make grade M=07         # module 07's tests against YOUR starter (must fail)
make solve M=07         # module 07's problem bank against YOUR stubs (must fail)
make labs               # every debug lab must exit 0
make progress           # how many of the 118 problems you have solved
```

---

## What Makes A Problem Here Different

Every problem's tests assert the property, not just the happy path:

- **Edge cases are named.** Empty input, a single element, all-equal values,
  duplicates, negatives — each with a comment saying which implementation bug it
  catches.
- **Scale is asserted.** Where the target is `O(n)`, a test runs at a size an
  `O(n^2)` solution cannot survive. A correct-but-quadratic answer fails.
- **Answers are cross-checked.** Most problems verify against an independent
  brute force over the same data, so a plausible-looking wrong answer is caught
  by construction.
- **The traps are the lesson.** Problems 03 and 04 of Module 02 look identical
  and need different techniques; Module 11's knapsack fails silently if the loop
  runs the wrong way. Those pairings are deliberate.
