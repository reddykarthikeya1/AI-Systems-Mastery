# Data Structures & Algorithms — Master Roadmap (0 to 100)

Welcome to the definitive **Data Structures & Algorithms (DSA) Master Roadmap**. This curriculum combines the rigor of **NeetCode 150**, **Striver's A2Z DSA Sheet**, and **Blind 75** with systems-level engineering principles (CPU cache locality, memory allocators, and lock-free concurrency).

---

## The 15 Core Modules & Curated LeetCode Problem Sets

Each module is paired with foundational theory, production engineering projects, and curated LeetCode problems categorized by difficulty: **Easy 🟢**, **Medium 🟡**, **Hard 🔴**.

---

### [Module 01: Complexity Analysis & Memory Layout](Module_01_Complexity_Analysis_and_Memory_Layout/01_README.md)
- **Core Mental Model**: Asymptotic bounds ($O, \Omega, \Theta$), Amortized analysis (Accounting & Potential methods), RAM addressing, CPU cache lines (64 bytes), L1/L2/L3 cache misses, and branch prediction.
- **Essential LeetCode Problems**:
  1. [LeetCode 191: Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) 🟢 (Bit manipulation, Kernighan's algorithm)
  2. [LeetCode 136: Single Number](https://leetcode.com/problems/single-number/) 🟢 (XOR cancellation property)
  3. [LeetCode 268: Missing Number](https://leetcode.com/problems/missing-number/) 🟢 (Gauss summation vs XOR)
  4. [LeetCode 338: Counting Bits](https://leetcode.com/problems/counting-bits/) 🟢 (DP on bit representation)
  5. [LeetCode 7: Reverse Integer](https://leetcode.com/problems/reverse-integer/) 🟡 (Integer overflow boundaries)

---

### [Module 02: Arrays, Dynamic Arrays & Strings](Module_02_Arrays_Dynamic_Arrays_and_Strings/01_README.md)
- **Core Mental Model**: Contiguous storage, geometric array resizing ($O(1)$ amortized), CPython `PyListObject` over-allocation, string immutability, UTF-8 variable-length encodings, Two Pointers, and Sliding Window.
- **Essential LeetCode Problems**:
  1. [LeetCode 1: Two Sum](https://leetcode.com/problems/two-sum/) 🟢 (Hash map complement lookup)
  2. [LeetCode 121: Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) 🟢 (Running minimum single pass)
  3. [LeetCode 217: Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) 🟢 (Hash set vs sorting)
  4. [LeetCode 242: Valid Anagram](https://leetcode.com/problems/valid-anagram/) 🟢 (Frequency array counting)
  5. [LeetCode 49: Group Anagrams](https://leetcode.com/problems/group-anagrams/) 🟡 (Tuple frequency signature as hash key)
  6. [LeetCode 238: Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) 🟡 (Prefix and suffix product accumulators)
  7. [LeetCode 53: Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) 🟡 (Kadane's algorithm: dynamic sub-array reset)
  8. [LeetCode 167: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) 🟡 (Two pointers converging from ends)
  9. [LeetCode 15: 3Sum](https://leetcode.com/problems/3sum/) 🟡 (Sort + Two pointers with duplicate skipping)
  10. [LeetCode 11: Container With Most Water](https://leetcode.com/problems/container-with-most-water/) 🟡 (Greedy two pointer inward shift)
  11. [LeetCode 42: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) 🔴 (Two pointer max tracking vs monotonic stack)
  12. [LeetCode 3: Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) 🟡 (Sliding window with character index hash map)
  13. [LeetCode 424: Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) 🟡 (Sliding window with max frequency invariant)
  14. [LeetCode 76: Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) 🔴 (Hard dynamic sliding window with character fulfillment counter)
  15. [LeetCode 560: Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) 🟡 (Prefix sum with frequency map)

---

### [Module 03: Linked Lists & Node Structures](Module_03_Linked_Lists_and_Pointer_Manipulation/01_README.md)
- **Core Mental Model**: Discontinuous heap nodes, pointer chasing, sentinel dummy nodes, fast & slow pointer runner technique, and in-place link reversal.
- **Essential LeetCode Problems**:
  1. [LeetCode 206: Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) 🟢 (Iterative three-pointer swap)
  2. [LeetCode 21: Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) 🟢 (Dummy head pointer splice)
  3. [LeetCode 141: Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) 🟢 (Floyd's Tortoise and Hare)
  4. [LeetCode 142: Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) 🟡 (Mathematical cycle entry derivation)
  5. [LeetCode 19: Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) 🟡 (Two-pointer gap offset)
  6. [LeetCode 143: Reorder List](https://leetcode.com/problems/reorder-list/) 🟡 (Find mid + Reverse second half + Interleave)
  7. [LeetCode 23: Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) 🔴 (Min-heap priority queue vs Divide-and-Conquer)

---

### [Module 04: Stacks, Queues & Monotonic Structures](Module_04_Stacks_Queues_and_Monotonic_Structures/01_README.md)
- **Core Mental Model**: LIFO vs FIFO abstractions, function call stack frames, Monotonic Increasing/Decreasing Stacks for $O(N)$ Next Greater Element, circular ring buffers.
- **Essential LeetCode Problems**:
  1. [LeetCode 20: Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) 🟢 (Stack matching open/close symbols)
  2. [LeetCode 155: Min Stack](https://leetcode.com/problems/min-stack/) 🟡 (Parallel auxiliary min stack or encoded values)
  3. [LeetCode 150: Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) 🟡 (Stack postfix evaluation)
  4. [LeetCode 739: Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) 🟡 (Monotonic decreasing stack for next warmer day)
  5. [LeetCode 84: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) 🔴 (Monotonic stack boundary expansion)
  6. [LeetCode 239: Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) 🔴 (Monotonic decreasing Deque in $O(N)$)

---

### [Module 05: Hash Tables & Collision Resolution](Module_05_Hash_Tables_and_Collision_Resolution/01_README.md)
- **Core Mental Model**: Hash functions (MurmurHash, SIPHash), load factor $\alpha = N / M$, Separate Chaining vs Open Addressing (Linear probing, Quadratic probing, Robin Hood hashing), CPython dictionary compact array layout.
- **Essential LeetCode Problems**:
  1. [LeetCode 128: Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) 🟡 (Hash set sequence start detection in $O(N)$)
  2. [LeetCode 36: Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) 🟡 (Row, column, and sub-box hashing)
  3. [LeetCode 380: Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) 🟡 (Dynamic array + Hash map index lookup with swap-with-last)
  4. [LeetCode 41: First Missing Positive](https://leetcode.com/problems/first-missing-positive/) 🔴 (In-place array index hashing)

---

### [Module 06: Trees, Binary Search Trees & Balancing](Module_06_Trees_Binary_Search_Trees_and_Self_Balancing/01_README.md)
- **Core Mental Model**: Hierarchical structures, Depth-First Traversals (Inorder, Preorder, Postorder), Breadth-First Traversal (Level Order), BST invariants, Lowest Common Ancestor (LCA), AVL & Red-Black balancing rotations.
- **Essential LeetCode Problems**:
  1. [LeetCode 226: Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) 🟢 (Recursive child swap)
  2. [LeetCode 104: Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) 🟢 (DFS recursion depth)
  3. [LeetCode 100: Same Tree](https://leetcode.com/problems/same-tree/) 🟢 (Simultaneous traversal validation)
  4. [LeetCode 572: Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) 🟢 (Subtree isomorphism matching)
  5. [LeetCode 235: Lowest Common Ancestor of a BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) 🟡 (BST value split direction)
  6. [LeetCode 102: Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) 🟡 (Queue-based BFS level processing)
  7. [LeetCode 98: Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) 🟡 (Propagating $(-\infty, +\infty)$ bounds)
  8. [LeetCode 230: Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) 🟡 (Inorder traversal early stopping)
  9. [LeetCode 105: Construct Binary Tree from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) 🟡 (Root split and index slicing)
  10. [LeetCode 124: Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) 🔴 (Post-order gain calculation with global max)
  11. [LeetCode 297: Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) 🔴 (Preorder DFS serialization with sentinel nulls)

---

### [Module 07: Heaps, Priority Queues & Top-K Patterns](Module_07_Heaps_Priority_Queues_and_TopK_Patterns/01_README.md)
- **Core Mental Model**: Complete binary tree representation in arrays, `parent(i) = (i-1)//2`, Sift-Up, Sift-Down, Floyd's $O(N)$ Heapify, Min-Heap vs Max-Heap, streaming Top-K.
- **Essential LeetCode Problems**:
  1. [LeetCode 703: Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) 🟢 (Fixed size-K Min-Heap)
  2. [LeetCode 1046: Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) 🟢 (Max-Heap simulation)
  3. [LeetCode 973: K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) 🟡 (Max-heap of size K or QuickSelect)
  4. [LeetCode 215: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) 🟡 (QuickSelect $O(N)$ average vs Min-Heap $O(N \log K)$)
  5. [LeetCode 347: Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) 🟡 (Bucket sort $O(N)$ vs Min-Heap)
  6. [LeetCode 621: Task Scheduler](https://leetcode.com/problems/task-scheduler/) 🟡 (Max-Heap frequency scheduling with cooldown queue)
  7. [LeetCode 295: Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) 🔴 (Dual Heaps: Max-Heap for lower half + Min-Heap for upper half)

---

### [Module 08: Graph Algorithms: Traversals & DAGs](Module_08_Graph_Algorithms_Traversals_and_DAGs/01_README.md)
- **Core Mental Model**: Adjacency lists vs Adjacency matrices, BFS (shortest unweighted path, level exploration), DFS (backtracking, connected components), Directed Acyclic Graphs (DAGs), Topological Sorting (Kahn's algorithm with indegree array & DFS post-order), Cycle detection.
- **Essential LeetCode Problems**:
  1. [LeetCode 200: Number of Islands](https://leetcode.com/problems/number-of-islands/) 🟡 (Grid BFS/DFS connected components)
  2. [LeetCode 695: Max Area of Island](https://leetcode.com/problems/max-area-of-island/) 🟡 (Flood fill area accumulation)
  3. [LeetCode 133: Clone Graph](https://leetcode.com/problems/clone-graph/) 🟡 (Hash map mapping old nodes to new nodes with BFS/DFS)
  4. [LeetCode 207: Course Schedule](https://leetcode.com/problems/course-schedule/) 🟡 (Kahn's algorithm indegree cycle check)
  5. [LeetCode 210: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) 🟡 (Topological sort ordering return)
  6. [LeetCode 417: Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) 🟡 (Reverse BFS/DFS from ocean edges)
  7. [LeetCode 994: Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) 🟡 (Multi-source BFS time simulation)
  8. [LeetCode 127: Word Ladder](https://leetcode.com/problems/word-ladder/) 🔴 (Shortest transformation sequence via BFS)

---

### [Module 09: Graph Algorithms: Shortest Paths & MST](Module_09_Graph_Algorithms_Shortest_Paths_and_MST/01_README.md)
- **Core Mental Model**: Weighted graph algorithms, Dijkstra's algorithm (greedy vertex relaxation with min-heap), Bellman-Ford (negative weight detection), Floyd-Warshall (all-pairs shortest paths), Minimum Spanning Trees (Kruskal's with Disjoint Set Union vs Prim's).
- **Essential LeetCode Problems**:
  1. [LeetCode 743: Network Delay Time](https://leetcode.com/problems/network-delay-time/) 🟡 (Standard Dijkstra shortest path)
  2. [LeetCode 787: Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) 🟡 (Bellman-Ford / BFS with step constraints)
  3. [LeetCode 1584: Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) 🟡 (Prim's algorithm with min-heap vs Kruskal's with DSU)
  4. [LeetCode 778: Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) 🔴 (Modified Dijkstra minimax path)

---

### [Module 10: Dynamic Programming: 1D & Sequence Patterns](Module_10_Dynamic_Programming_1D_and_Sequence_Patterns/01_README.md)
- **Core Mental Model**: Optimal Substructure, Overlapping Subproblems, Top-Down Memoization vs Bottom-Up Tabulation, Space optimization ($O(N) \to O(1)$ variables), State transition recurrence relations.
- **Essential LeetCode Problems**:
  1. [LeetCode 70: Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) 🟢 (Base Fibonacci state transitions)
  2. [LeetCode 746: Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) 🟢 (Cost accumulation recurrence)
  3. [LeetCode 198: House Robber](https://leetcode.com/problems/house-robber/) 🟡 (Pick or Skip non-adjacent state transitions)
  4. [LeetCode 213: House Robber II](https://leetcode.com/problems/house-robber-ii/) 🟡 (Circular array state decomposition)
  5. [LeetCode 5: Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) 🟡 (Expand around center or 2D DP table)
  6. [LeetCode 322: Coin Change](https://leetcode.com/problems/coin-change/) 🟡 (Unbounded knapsack minimum steps)
  7. [LeetCode 139: Word Break](https://leetcode.com/problems/word-break/) 🟡 (Boolean prefix matching DP)
  8. [LeetCode 300: Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) 🟡 ($O(N^2)$ DP vs $O(N \log N)$ Patience Sorting with Binary Search)
  9. [LeetCode 152: Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) 🟡 (Tracking min and max products for negative flips)

---

### [Module 11: Dynamic Programming: 2D, Knapsack & Grids](Module_11_Dynamic_Programming_2D_Knapsack_and_Grids/01_README.md)
- **Core Mental Model**: Multi-dimensional state spaces $DP[i][j]$, 0/1 Knapsack (item inclusion/exclusion), Grid traversal paths, String alignment matrices (Edit Distance, Longest Common Subsequence).
- **Essential LeetCode Problems**:
  1. [LeetCode 62: Unique Paths](https://leetcode.com/problems/unique-paths/) 🟡 (Grid path sum recurrence)
  2. [LeetCode 1143: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) 🟡 (Character match diagonal vs adjacent max)
  3. [LeetCode 72: Edit Distance](https://leetcode.com/problems/edit-distance/) 🟡 (Levenshtein distance: insert, delete, replace operations)
  4. [LeetCode 518: Coin Change II](https://leetcode.com/problems/coin-change-ii/) 🟡 (Combinatorial count unbounded knapsack)
  5. [LeetCode 416: Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) 🟡 (0/1 Knapsack target sum reduction)
  6. [LeetCode 309: Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) 🟡 (Finite State Machine DP: Held, Sold, Cooldown states)
  7. [LeetCode 312: Burst Balloons](https://leetcode.com/problems/burst-balloons/) 🔴 (Interval DP: choosing the last balloon to burst)

---

### [Module 12: Greedy Algorithms & Interval Scheduling](Module_12_Greedy_Algorithms_and_Interval_Scheduling/01_README.md)
- **Core Mental Model**: Greedy Choice Property, Optimal Substructure, Proving greedy correctness via exchange arguments, Interval sorting by start/end times, Sweep-line techniques.
- **Essential LeetCode Problems**:
  1. [LeetCode 55: Jump Game](https://leetcode.com/problems/jump-game/) 🟡 (Greedy maximum reach boundary tracking)
  2. [LeetCode 45: Jump Game II](https://leetcode.com/problems/jump-game-ii/) 🟡 (Breadth-first greedy jump intervals)
  3. [LeetCode 56: Merge Intervals](https://leetcode.com/problems/merge-intervals/) 🟡 (Sort by start time + Overlap expansion)
  4. [LeetCode 57: Insert Interval](https://leetcode.com/problems/insert-interval/) 🟡 (Linear sweep three-phase partition)
  5. [LeetCode 435: Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) 🟡 (Greedy earliest finish time scheduling)
  6. [LeetCode 763: Partition Labels](https://leetcode.com/problems/partition-labels/) 🟡 (Last occurrence boundary tracking)
  7. [LeetCode 134: Gas Station](https://leetcode.com/problems/gas-station/) 🟡 (Total surplus vs local deficit greedy start)

---

### [Module 13: Backtracking & Constraint Satisfaction](Module_13_Backtracking_and_Constraint_Satisfaction/01_README.md)
- **Core Mental Model**: State space tree exploration, Depth-First search with state modification and undoing, Pruning invalid subtrees early, Permutations vs Combinations vs Subsets.
- **Essential LeetCode Problems**:
  1. [LeetCode 78: Subsets](https://leetcode.com/problems/subsets/) 🟡 (Cascading inclusion/exclusion tree)
  2. [LeetCode 90: Subsets II](https://leetcode.com/problems/subsets-ii/) 🟡 (Handling duplicates with sort and skip)
  3. [LeetCode 39: Combination Sum](https://leetcode.com/problems/combination-sum/) 🟡 (Unbounded element picking with remaining sum target)
  4. [LeetCode 40: Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) 🟡 (Single use per element with duplicate branch pruning)
  5. [LeetCode 46: Permutations](https://leetcode.com/problems/permutations/) 🟡 (Visited tracking or in-place element swapping)
  6. [LeetCode 79: Word Search](https://leetcode.com/problems/word-search/) 🟡 (2D Grid DFS backtracking with visited marker)
  7. [LeetCode 131: Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) 🟡 (Prefix palindrome check + recursive suffix split)
  8. [LeetCode 51: N-Queens](https://leetcode.com/problems/n-queens/) 🔴 (Column, positive diagonal, negative diagonal bit/set tracking)

---

### [Module 14: Advanced Structures: Trie, Union-Find & Segment Trees](Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/01_README.md)
- **Core Mental Model**: Prefix trees (Tries) for string lookups, Disjoint Set Union (DSU) with Path Compression and Union by Rank for near-$O(1)$ dynamic connectivity, Segment Trees & Fenwick Trees for $O(\log N)$ dynamic range sum/min queries.
- **Essential LeetCode Problems**:
  1. [LeetCode 208: Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) 🟡 (TrieNode children dictionary and terminal flag)
  2. [LeetCode 211: Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) 🟡 (Trie search with wildcard '.' backtracking)
  3. [LeetCode 212: Word Search II](https://leetcode.com/problems/word-search-ii/) 🔴 (2D Grid backtracking guided by Trie prefix pruning)
  4. [LeetCode 684: Redundant Connection](https://leetcode.com/problems/redundant-connection/) 🟡 (DSU cycle detection on undirected graph)
  5. [LeetCode 307: Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) 🟡 (Segment Tree or Binary Indexed Tree)
  6. [LeetCode 327: Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) 🔴 (Merge sort / Segment tree on prefix sums)

---

### [Module 15: Systems-Level Algorithmic Data Structures](Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU/01_README.md)
- **Core Mental Model**: Bridging algorithmic interview puzzles to production software engines. Probabilistic data structures (Skip Lists, Bloom Filters, HyperLogLog), cache eviction algorithms (LRU, LFU, ARC), and concurrency (Lock-Free Queues, Ring Buffers).
- **Essential LeetCode & Systems Problems**:
  1. [LeetCode 146: LRU Cache](https://leetcode.com/problems/lru-cache/) 🟡 (Doubly Linked List + Hash Map for $O(1)$ get and put)
  2. [LeetCode 460: LFU Cache](https://leetcode.com/problems/lfu-cache/) 🔴 (Frequency Map + Doubly Linked Lists for $O(1)$ frequency eviction)
  3. [LeetCode 1206: Design Skiplist](https://leetcode.com/problems/design-skiplist/) 🔴 (Probabilistic multi-level forward pointers)
  4. [LeetCode 641: Design Circular Deque](https://leetcode.com/problems/design-circular-deque/) 🟡 (Modulo index arithmetic array)
  5. [LeetCode 1188: Design Bounded Blocking Queue](https://leetcode.com/problems/design-bounded-blocking-queue/) 🟡 (Thread synchronization with condition variables)

---

## Strategic Pacing Plans

```
INTENSIVE CRUNCH (4 WEEKS)         STANDARD MASTERY (8 WEEKS)        DEEP SYSTEMS EXPERT (16 WEEKS)
├─ Week 1: Modules 01 - 04         ├─ Weeks 1-2: Modules 01 - 04     ├─ Month 1: Modules 01 - 05
├─ Week 2: Modules 05 - 07         ├─ Weeks 3-4: Modules 05 - 07     ├─ Month 2: Modules 06 - 09
├─ Week 3: Modules 08 - 11         ├─ Weeks 5-6: Modules 08 - 11     ├─ Month 3: Modules 10 - 13
└─ Week 4: Modules 12 - 15         └─ Weeks 7-8: Modules 12 - 15     └─ Month 4: Modules 14 - 15
```
