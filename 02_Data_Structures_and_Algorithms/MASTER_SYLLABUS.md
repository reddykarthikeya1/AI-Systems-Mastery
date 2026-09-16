# Master Syllabus: Data Structures & Algorithms (0 to 100)

> 17 Modules · 17 Production Projects · [DSA Master Interactive Roadmap](ROADMAP_DSA_MASTER.md)

## Course Overview Matrix

| Module | Title | Core Topics | Project Focus |
|---|---|---|---|
| **01** | [Complexity Analysis & Memory Layout](Module_01_Complexity_Analysis_and_Memory_Layout/01_README.md) | Big-O, Big-Omega, Amortized Analysis, CPU Cache Locality, and Branch Prediction | [Complexity Analysis & Memory Layout Engine](Module_01_Complexity_Analysis_and_Memory_Layout/04_PROJECT_GUIDE.md) |
| **02** | [Arrays, Dynamic Arrays & Strings](Module_02_Arrays_Dynamic_Arrays_and_Strings/01_README.md) | Memory Reallocation, Resizing Amortization, Two-Pointers, and Sliding Window | [Arrays, Dynamic Arrays & Strings Engine](Module_02_Arrays_Dynamic_Arrays_and_Strings/07_PROJECT_GUIDE.md) |
| **03** | [Linked Lists & Node Structures](Module_03_Linked_Lists_and_Pointer_Manipulation/01_README.md) | Singly/Doubly Linked Lists, Fast & Slow Pointers, Cycle Detection, and Reverse Operations | [Linked Lists & Node Structures Engine](Module_03_Linked_Lists_and_Pointer_Manipulation/04_PROJECT_GUIDE.md) |
| **04** | [Stacks, Queues & Monotonic Structures](Module_04_Stacks_Queues_and_Monotonic_Structures/01_README.md) | LIFO/FIFO Internals, Monotonic Stacks, Deques, and Sliding Window Maximum | [Stacks, Queues & Monotonic Structures Engine](Module_04_Stacks_Queues_and_Monotonic_Structures/04_PROJECT_GUIDE.md) |
| **05** | [Hash Tables & Collision Resolution](Module_05_Hash_Tables_and_Collision_Resolution/01_README.md) | Hash Functions, Separate Chaining, Open Addressing, Robin Hood Hashing, and CPython Dict Internals | [Hash Tables & Collision Resolution Engine](Module_05_Hash_Tables_and_Collision_Resolution/04_PROJECT_GUIDE.md) |
| **06** | [Trees, BSTs & Balancing](Module_06_Trees_Binary_Search_Trees_and_Self_Balancing/01_README.md) | Tree Traversals (In/Pre/Post/Level), LCA, BST Invariants, and AVL/Red-Black Balancing Intuitions | [Trees, BSTs & Balancing Engine](Module_06_Trees_Binary_Search_Trees_and_Self_Balancing/04_PROJECT_GUIDE.md) |
| **07** | [Heaps & Priority Queues](Module_07_Heaps_Priority_Queues_and_TopK_Patterns/01_README.md) | Binary Heaps, Heapify in O(N), Median of Streaming Data, and K-Way Merging | [Heaps & Priority Queues Engine](Module_07_Heaps_Priority_Queues_and_TopK_Patterns/04_PROJECT_GUIDE.md) |
| **08** | [Graph Traversals & DAGs](Module_08_Graph_Algorithms_Traversals_and_DAGs/01_README.md) | Adjacency Representations, BFS, DFS, Topological Sorting, and Cycle Detection | [Graph Traversals & DAGs Engine](Module_08_Graph_Algorithms_Traversals_and_DAGs/04_PROJECT_GUIDE.md) |
| **09** | [Shortest Paths & Minimum Spanning Trees](Module_09_Graph_Algorithms_Shortest_Paths_and_MST/01_README.md) | Dijkstra with Heaps, Bellman-Ford, A* Search, Kruskal with DSU, and Prim's Algorithm | [Shortest Paths & Minimum Spanning Trees Engine](Module_09_Graph_Algorithms_Shortest_Paths_and_MST/04_PROJECT_GUIDE.md) |
| **10** | [Dynamic Programming: 1D & Sequences](Module_10_Dynamic_Programming_1D_and_Sequence_Patterns/01_README.md) | Memoization vs Tabulation, State Space Transitions, Fibonacci to Longest Increasing Subsequence | [Dynamic Programming: 1D & Sequences Engine](Module_10_Dynamic_Programming_1D_and_Sequence_Patterns/04_PROJECT_GUIDE.md) |
| **11** | [Dynamic Programming: 2D & Knapsack](Module_11_Dynamic_Programming_2D_Knapsack_and_Grids/01_README.md) | 0/1 Knapsack, Unbounded Knapsack, Edit Distance, Longest Common Subsequence, and Grid Paths | [Dynamic Programming: 2D & Knapsack Engine](Module_11_Dynamic_Programming_2D_Knapsack_and_Grids/04_PROJECT_GUIDE.md) |
| **12** | [Greedy Algorithms & Intervals](Module_12_Greedy_Algorithms_and_Interval_Scheduling/01_README.md) | Greedy Choice Property, Interval Merging, Fractional Knapsack, and Huffman Coding | [Greedy Algorithms & Intervals Engine](Module_12_Greedy_Algorithms_and_Interval_Scheduling/04_PROJECT_GUIDE.md) |
| **13** | [Backtracking & State Search](Module_13_Backtracking_and_Constraint_Satisfaction/01_README.md) | State Space Trees, N-Queens, Sudoku Solver, Subset Sum, and Pruning Optimizations | [Backtracking & State Search Engine](Module_13_Backtracking_and_Constraint_Satisfaction/04_PROJECT_GUIDE.md) |
| **14** | [Advanced Trees & Sets](Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/01_README.md) | Trie (Prefix Trees), Disjoint Set Union (Union-Find with Path Compression), and Segment Trees | [Advanced Trees & Sets Engine](Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/04_PROJECT_GUIDE.md) |
| **15** | [Systems Data Structures](Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU/01_README.md) | Skip Lists, Bloom Filters, HyperLogLog, Ring Buffers, and O(1) LRU/LFU Cache Eviction | [Systems Data Structures Engine](Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU/04_PROJECT_GUIDE.md) |

---

## Practice Infrastructure

Beyond the 15 module projects, the course ships a pattern-indexed problem bank
and a diagnostic lab per module.

| Artifact | Count | Purpose |
| :--- | :---: | :--- |
| [Pattern Recognition Guide](PATTERN_RECOGNITION_GUIDE.md) | 1 | The decision procedure: constraints → complexity → technique |
| Problem bank (`Module_*/problems/`) | **118 problems** | Recall, with hint ladders and verified solutions |
| Debug labs (`Module_*/debug_lab/`) | 15 labs, 56 defects | Diagnosis — every defect exits 0 |
| [Phase checkpoints](Phase_Checkpoints/PHASE_01_CHECKPOINT.md) | 7 | Gates that need the phase's material, not a quiz |

### Pattern coverage

| Pattern | Drilled in |
| :--- | :--- |
| Two pointers, sliding window, prefix sums, binary search on the answer | [Module 02](Module_02_Arrays_Dynamic_Arrays_and_Strings/problems/README.md) |
| Fast/slow pointers, dummy head, in-place reversal | [Module 03](Module_03_Linked_Lists_and_Pointer_Manipulation/problems/README.md) |
| Monotonic stack and deque | [Module 04](Module_04_Stacks_Queues_and_Monotonic_Structures/problems/README.md) |
| Hash-map complements, canonical keys, counting | [Module 05](Module_05_Hash_Tables_and_Collision_Resolution/problems/README.md) |
| Tree traversal, BST range invariants | [Module 06](Module_06_Trees_Binary_Search_Trees_and_Self_Balancing/problems/README.md) |
| Heaps, top-k, streaming median | [Module 07](Module_07_Heaps_Priority_Queues_and_TopK_Patterns/problems/README.md) |
| BFS, DFS, three-colour cycle detection, topological sort | [Module 08](Module_08_Graph_Algorithms_Traversals_and_DAGs/problems/README.md) |
| Dijkstra, Bellman-Ford, Kruskal, Prim | [Module 09](Module_09_Graph_Algorithms_Shortest_Paths_and_MST/problems/README.md) |
| 1D DP, state machines, two-value state | [Module 10](Module_10_Dynamic_Programming_1D_and_Sequence_Patterns/problems/README.md) |
| 2D DP, knapsack, interval DP, rolling arrays | [Module 11](Module_11_Dynamic_Programming_2D_Knapsack_and_Grids/problems/README.md) |
| Greedy, exchange arguments, interval ordering | [Module 12](Module_12_Greedy_Algorithms_and_Interval_Scheduling/problems/README.md) |
| Backtracking, pruning, duplicate skipping | [Module 13](Module_13_Backtracking_and_Constraint_Satisfaction/problems/README.md) |
| Trie, union-find, segment tree, Fenwick, sparse table | [Module 14](Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/problems/README.md) |
| LRU/LFU, Bloom, HyperLogLog, Count-Min, consistent hashing | [Module 15](Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU/problems/README.md) |
