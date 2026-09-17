"""
Trace Data Generator
Generates authentic, schema-compliant trace.json files across all 17 modules
of 02_Data_Structures_and_Algorithms for the AlgorithmTraceScrubber component.
"""

import json
import os
from pathlib import Path

MODULE_TRACES = {
    "Module_01_Complexity_Analysis_and_Memory_Layout": {
        "title": "CPU Memory Hierarchy & Cache Line Latency Trace",
        "algorithm": "Memory Access Stride (Cache Line Snooping)",
        "timeComplexity": "O(1) cache hit vs O(100) DRAM stall",
        "spaceComplexity": "64-byte Cache Lines",
        "frames": [
            {
                "step": 1,
                "description": "Sequential memory access at offset 0x00: L1 Cache Hit (4 clock cycles, 1.0 ns).",
                "array": [64, 128, 192, 256, 320, 384, 448, 512],
                "pointers": { "offset": 0 },
                "highlights": { "0": "sorted" },
                "variables": { "address": "0x7fff00", "latency_ns": 1.0, "level": "L1 Data Cache", "hit": True },
                "invariants": "Stride-1 access accesses spatial cache line already residing in L1"
            },
            {
                "step": 2,
                "description": "Access offset 0x40 (Next 64B cache line): L1 line fill prefetched from L2.",
                "array": [64, 128, 192, 256, 320, 384, 448, 512],
                "pointers": { "offset": 1 },
                "highlights": { "0": "sorted", "1": "active" },
                "variables": { "address": "0x7fff40", "latency_ns": 3.5, "level": "L2 Cache", "hit": True },
                "invariants": "Hardware prefetcher tracks sequential access stream"
            },
            {
                "step": 3,
                "description": "Strided jump to offset 0x1000 (4KB stride): L1/L2/L3 Cache Miss! DRAM access stalled.",
                "array": [64, 128, 192, 256, 320, 384, 448, 512],
                "pointers": { "offset": 7 },
                "highlights": { "0": "sorted", "7": "pivot" },
                "variables": { "address": "0x7fff1000", "latency_ns": 85.0, "level": "Main Memory (DRAM)", "hit": False },
                "invariants": "DRAM roundtrip incurs 200+ CPU cycle pipeline bubble"
            }
        ]
    },

    "Module_02_Arrays_Dynamic_Arrays_and_Strings": {
        "title": "Two Pointers Search Verification: Two Sum II",
        "algorithm": "Two Pointers on Sorted Array",
        "timeComplexity": "O(n)",
        "spaceComplexity": "O(1)",
        "frames": [
            {
                "step": 1,
                "description": "Initialize left=0 and right=5. Sum = 2 + 20 = 22 > 18 (Target = 18).",
                "array": [2, 4, 7, 11, 14, 20],
                "pointers": { "left": 0, "right": 5 },
                "highlights": { "0": "active", "5": "active" },
                "variables": { "left": 0, "right": 5, "currentSum": 22, "target": 18 },
                "invariants": "Current sum (22) > target (18): Decrement right pointer to reduce sum"
            },
            {
                "step": 2,
                "description": "Decrement right to index 4. Sum = 2 + 14 = 16 < 18.",
                "array": [2, 4, 7, 11, 14, 20],
                "pointers": { "left": 0, "right": 4 },
                "highlights": { "0": "active", "4": "active" },
                "variables": { "left": 0, "right": 4, "currentSum": 16, "target": 18 },
                "invariants": "Current sum (16) < target (18): Increment left pointer to increase sum"
            },
            {
                "step": 3,
                "description": "Increment left to index 1. Sum = 4 + 14 = 18 === target! Target pair found.",
                "array": [2, 4, 7, 11, 14, 20],
                "pointers": { "left": 1, "right": 4 },
                "highlights": { "1": "sorted", "4": "sorted" },
                "variables": { "left": 1, "right": 4, "currentSum": 18, "target": 18, "found": True },
                "invariants": "Target match verified: return indices [1, 4] (1-indexed: [2, 5])"
            }
        ]
    },

    "Module_03_Linked_Lists_and_Pointer_Manipulation": {
        "title": "Floyd's Tortoise and Hare Cycle Detection",
        "algorithm": "Two Pointers Fast & Slow",
        "timeComplexity": "O(n)",
        "spaceComplexity": "O(1)",
        "frames": [
            {
                "step": 1,
                "description": "Initialize slow=0 and fast=0 at list head.",
                "array": [10, 20, 30, 40, 50, 30],
                "pointers": { "slow": 0, "fast": 0 },
                "highlights": { "0": "active" },
                "variables": { "slowIdx": 0, "fastIdx": 0, "cycleDetected": False },
                "invariants": "Distance between fast and slow increases by 1 each iteration"
            },
            {
                "step": 2,
                "description": "slow advances 1 step (idx 1), fast advances 2 steps (idx 2).",
                "array": [10, 20, 30, 40, 50, 30],
                "pointers": { "slow": 1, "fast": 2 },
                "highlights": { "1": "comparing", "2": "active" },
                "variables": { "slowIdx": 1, "fastIdx": 2, "cycleDetected": False },
                "invariants": "Fast traverses 2x faster than slow"
            },
            {
                "step": 3,
                "description": "Fast wraps around cycle: slow at idx 3, fast loops back to idx 3! Pointers collide.",
                "array": [10, 20, 30, 40, 50, 30],
                "pointers": { "slow": 3, "fast": 3 },
                "highlights": { "3": "sorted" },
                "variables": { "slowIdx": 3, "fastIdx": 3, "cycleDetected": True },
                "invariants": "Fast and slow collision proves existence of cycle in O(n) time"
            }
        ]
    },

    "Module_04_Stacks_Queues_and_Monotonic_Structures": {
        "title": "Monotonic Decreasing Stack: Next Greater Element",
        "algorithm": "Monotonic Stack Evaluation",
        "timeComplexity": "O(n)",
        "spaceComplexity": "O(n)",
        "frames": [
            {
                "step": 1,
                "description": "Process element 2 (idx 0). Stack is empty -> push 0.",
                "array": [2, 1, 5, 6, 2, 3],
                "pointers": { "curr": 0 },
                "highlights": { "0": "active" },
                "variables": { "stack": [0], "val": 2 },
                "invariants": "Stack stores indices of elements waiting for next greater target"
            },
            {
                "step": 2,
                "description": "Process element 1 (idx 1). 1 < 2 -> push 1. Stack = [0, 1].",
                "array": [2, 1, 5, 6, 2, 3],
                "pointers": { "curr": 1 },
                "highlights": { "0": "active", "1": "active" },
                "variables": { "stack": [0, 1], "val": 1 },
                "invariants": "Decreasing order maintained: array[0] (2) >= array[1] (1)"
            },
            {
                "step": 3,
                "description": "Process element 5 (idx 2). 5 > 1: Pop 1! 5 > 2: Pop 0! Next greater of 1 and 2 is 5.",
                "array": [2, 1, 5, 6, 2, 3],
                "pointers": { "curr": 2 },
                "highlights": { "0": "sorted", "1": "sorted", "2": "pivot" },
                "variables": { "stack": [2], "val": 5, "popped": [1, 0] },
                "invariants": "Each element is pushed and popped at most once -> Amortized O(n)"
            }
        ]
    },

    "Module_05_Hash_Tables_and_Collision_Resolution": {
        "title": "Robin Hood Hashing Probe Sequence Length (PSL)",
        "algorithm": "Open Addressing with Robin Hood Swaps",
        "timeComplexity": "O(1) average",
        "spaceComplexity": "O(n)",
        "frames": [
            {
                "step": 1,
                "description": "Insert Key 'X' (ideal index 1). Slot 1 is occupied by 'A' (PSL=0). 'X' PSL becomes 1.",
                "array": ["KeyA (0)", "KeyX (1)", "Empty", "Empty", "Empty"],
                "pointers": { "probe": 1 },
                "highlights": { "0": "active", "1": "comparing" },
                "variables": { "incomingKey": "X", "incomingPSL": 1, "occupantPSL": 0 },
                "invariants": "incomingPSL (1) > occupantPSL (0) -> Robin Hood displacement swap!"
            },
            {
                "step": 2,
                "description": "Key 'X' takes slot 1. Displaced 'A' probes next slot 2 with PSL 1.",
                "array": ["KeyA (0)", "KeyX (0)", "KeyA (1)", "Empty", "Empty"],
                "pointers": { "probe": 2 },
                "highlights": { "1": "sorted", "2": "active" },
                "variables": { "slot1": "KeyX", "slot2": "KeyA", "displaced": True },
                "invariants": "Robin Hood reduces variance of search times across keys"
            }
        ]
    },

    "Module_06_Trees_Binary_Search_Trees_and_Self_Balancing": {
        "title": "Binary Search Tree Key Search & Invariant",
        "algorithm": "BST Divide-and-Conquer Search",
        "timeComplexity": "O(log n)",
        "spaceComplexity": "O(1)",
        "frames": [
            {
                "step": 1,
                "description": "Target is 25. Compare with Root (30). 25 < 30 -> Traverse Left.",
                "array": [30, 15, 45, 10, 25, 35, 60],
                "pointers": { "curr": 0 },
                "highlights": { "0": "comparing" },
                "variables": { "target": 25, "currKey": 30, "action": "go_left" },
                "invariants": "All keys in left subtree are strictly less than current node key"
            },
            {
                "step": 2,
                "description": "Compare with Node (15). 25 > 15 -> Traverse Right.",
                "array": [30, 15, 45, 10, 25, 35, 60],
                "pointers": { "curr": 1 },
                "highlights": { "1": "comparing" },
                "variables": { "target": 25, "currKey": 15, "action": "go_right" },
                "invariants": "All keys in right subtree are strictly greater than current node key"
            },
            {
                "step": 3,
                "description": "Compare with Node (25). 25 === 25 -> Key Found in 3 steps!",
                "array": [30, 15, 45, 10, 25, 35, 60],
                "pointers": { "curr": 4 },
                "highlights": { "4": "sorted" },
                "variables": { "target": 25, "currKey": 25, "found": True },
                "invariants": "Search completed in O(h) comparisons where h = tree height"
            }
        ]
    },

    "Module_07_Heaps_Priority_Queues_and_TopK_Patterns": {
        "title": "Binary Min-Heap Sift-Down Invariant Scrubber",
        "algorithm": "Binary Heap Sift-Down",
        "timeComplexity": "O(log n)",
        "spaceComplexity": "O(1)",
        "frames": [
            {
                "step": 1,
                "description": "Root has invalid high value 50 after extract-min. Check children 4 and 7.",
                "array": [50, 4, 7, 12, 15, 20, 30],
                "pointers": { "parent": 0, "child": 1 },
                "highlights": { "0": "pivot", "1": "active", "2": "comparing" },
                "variables": { "parentVal": 50, "leftVal": 4, "rightVal": 7, "minChild": 4 },
                "invariants": "Left child (4) is smaller than parent (50) -> Swap required"
            },
            {
                "step": 2,
                "description": "Swapped 50 and 4. Parent at idx 1. Check children 12 and 15.",
                "array": [4, 50, 7, 12, 15, 20, 30],
                "pointers": { "parent": 1, "child": 3 },
                "highlights": { "1": "pivot", "3": "active", "4": "comparing" },
                "variables": { "parentVal": 50, "leftVal": 12, "rightVal": 15, "minChild": 12 },
                "invariants": "Child (12) is smaller than parent (50) -> Swap required"
            },
            {
                "step": 3,
                "description": "Swapped 50 and 12. Index 3 is a leaf. Min-heap invariant restored!",
                "array": [4, 12, 7, 50, 15, 20, 30],
                "pointers": { "parent": 3 },
                "highlights": { "0": "sorted", "1": "sorted", "2": "sorted", "3": "sorted" },
                "variables": { "parentVal": 50, "heapPropertyRestored": True },
                "invariants": "Min-heap condition satisfied: parent <= both children"
            }
        ]
    },

    "Module_08_Graph_Algorithms_Traversals_and_DAGs": {
        "title": "Kahn's Algorithm BFS Topological Sort",
        "algorithm": "Topological Sort via In-Degree Queue",
        "timeComplexity": "O(V + E)",
        "spaceComplexity": "O(V)",
        "frames": [
            {
                "step": 1,
                "description": "Compute in-degrees: Node 0 in-degree is 0. Push 0 into queue.",
                "array": ["Node 0 (in:0)", "Node 1 (in:1)", "Node 2 (in:1)", "Node 3 (in:2)"],
                "pointers": { "queue": 0 },
                "highlights": { "0": "active" },
                "variables": { "queue": [0], "topoOrder": [] },
                "invariants": "Nodes with 0 incoming dependencies are ready for scheduling"
            },
            {
                "step": 2,
                "description": "Pop Node 0, append to order. Decrement in-degree of Node 1 and 2 to 0! Push both.",
                "array": ["Node 0 (done)", "Node 1 (in:0)", "Node 2 (in:0)", "Node 3 (in:2)"],
                "pointers": { "queue": 1 },
                "highlights": { "0": "sorted", "1": "active", "2": "active" },
                "variables": { "queue": [1, 2], "topoOrder": [0] },
                "invariants": "Removing processed node reduces dependency counts of immediate neighbors"
            },
            {
                "step": 3,
                "description": "Process Nodes 1 and 2. Node 3 in-degree reaches 0. All 4 nodes processed!",
                "array": ["Node 0 (done)", "Node 1 (done)", "Node 2 (done)", "Node 3 (done)"],
                "pointers": { "queue": 3 },
                "highlights": { "0": "sorted", "1": "sorted", "2": "sorted", "3": "sorted" },
                "variables": { "topoOrder": [0, 1, 2, 3], "isDAG": True },
                "invariants": "Processed node count == V proves graph is a valid DAG (no cycles)"
            }
        ]
    },

    "Module_09_Graph_Algorithms_Shortest_Paths_and_MST": {
        "title": "Dijkstra Shortest Path Relaxation Frontier",
        "algorithm": "Dijkstra with Priority Queue",
        "timeComplexity": "O((V + E) log V)",
        "spaceComplexity": "O(V)",
        "frames": [
            {
                "step": 1,
                "description": "Initialize Start node S with dist=0. All other nodes dist=∞. Pop S from PQ.",
                "array": ["S: 0", "A: ∞", "B: ∞", "C: ∞", "T: ∞"],
                "pointers": { "curr": 0 },
                "highlights": { "0": "pivot" },
                "variables": { "activeNode": "S", "activeDist": 0 },
                "invariants": "Priority queue extracts globally minimum tentative distance"
            },
            {
                "step": 2,
                "description": "Relax neighbors of S: A becomes 4 (0+4), B becomes 2 (0+2). Pop B (min dist 2).",
                "array": ["S: 0", "A: 4", "B: 2", "C: ∞", "T: ∞"],
                "pointers": { "curr": 2 },
                "highlights": { "0": "sorted", "1": "comparing", "2": "pivot" },
                "variables": { "activeNode": "B", "activeDist": 2 },
                "invariants": "Edge relaxation: if dist[u] + w < dist[v], update dist[v]"
            },
            {
                "step": 3,
                "description": "Relax edge B -> A with weight 1: dist[A] updates 4 -> 3! Shortest path to A is via B.",
                "array": ["S: 0", "A: 3", "B: 2", "C: 7", "T: ∞"],
                "pointers": { "curr": 1 },
                "highlights": { "0": "sorted", "1": "sorted", "2": "sorted" },
                "variables": { "activeNode": "A", "improved": True },
                "invariants": "Optimal substructure property: sub-paths of shortest paths are shortest paths"
            }
        ]
    },

    "Module_10_Dynamic_Programming_1D_and_Sequence_Patterns": {
        "title": "Kadane's Algorithm Maximum Subarray Sum",
        "algorithm": "Dynamic Programming: Kadane",
        "timeComplexity": "O(n)",
        "spaceComplexity": "O(1)",
        "frames": [
            {
                "step": 1,
                "description": "Element 0: val = -2. currentMax = -2, globalMax = -2.",
                "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
                "pointers": { "i": 0 },
                "highlights": { "0": "active" },
                "variables": { "num": -2, "currentMax": -2, "globalMax": -2 },
                "invariants": "dp[i] = max(nums[i], dp[i-1] + nums[i])"
            },
            {
                "step": 2,
                "description": "Element 1: val = 1. max(1, -2+1) = 1. Reset subarray start! globalMax = 1.",
                "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
                "pointers": { "i": 1 },
                "highlights": { "1": "sorted" },
                "variables": { "num": 1, "currentMax": 1, "globalMax": 1 },
                "invariants": "Negative prefix discarded because starting fresh at 1 yields larger sum"
            },
            {
                "step": 3,
                "description": "Elements 3 through 6: Contiguous block [4, -1, 2, 1] accumulates maximum sum = 6!",
                "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
                "pointers": { "start": 3, "end": 6 },
                "highlights": { "3": "sorted", "4": "sorted", "5": "sorted", "6": "sorted" },
                "variables": { "subArraySum": 6, "globalMax": 6 },
                "invariants": "Global maximum subarray sum identified: 6 (range [3..6])"
            }
        ]
    },

    "Module_11_Dynamic_Programming_2D_Knapsack_and_Grids": {
        "title": "0/1 Knapsack State Space Transition",
        "algorithm": "2D Dynamic Programming",
        "timeComplexity": "O(N * W)",
        "spaceComplexity": "O(W)",
        "frames": [
            {
                "step": 1,
                "description": "Item 1 (wt: 2, val: 3). Capacities w < 2 cannot take item. Capacities >= 2 store 3.",
                "array": ["w=0: 0", "w=1: 0", "w=2: 3", "w=3: 3", "w=4: 3"],
                "pointers": { "w": 2 },
                "highlights": { "2": "active" },
                "variables": { "item": 1, "wt": 2, "val": 3 },
                "invariants": "Base transition: dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt] + val)"
            },
            {
                "step": 2,
                "description": "Item 2 (wt: 3, val: 4). At capacity w=4, can include Item 2 (wt 3) + Item 1 (wt 1 impossible).",
                "array": ["w=0: 0", "w=1: 0", "w=2: 3", "w=3: 4", "w=4: 4"],
                "pointers": { "w": 3 },
                "highlights": { "3": "active" },
                "variables": { "item": 2, "wt": 3, "val": 4 },
                "invariants": "Compare excluding item 2 (val 3) vs including item 2 (val 4) -> Choose 4"
            },
            {
                "step": 3,
                "description": "Item 3 (wt: 1, val: 2). At capacity w=4: take Item 3 (wt 1) + Item 2 (wt 3) = val 6! Optimal!",
                "array": ["w=0: 0", "w=1: 2", "w=2: 3", "w=3: 5", "w=4: 6"],
                "pointers": { "w": 4 },
                "highlights": { "4": "sorted" },
                "variables": { "maxVal": 6, "capacity": 4 },
                "invariants": "Optimal solution: total value 6 with weight 4"
            }
        ]
    },

    "Module_12_Greedy_Algorithms_and_Interval_Scheduling": {
        "title": "Greedy Interval Scheduling: Earliest Finish Time",
        "algorithm": "Greedy Activity Selection",
        "timeComplexity": "O(n log n)",
        "spaceComplexity": "O(1)",
        "frames": [
            {
                "step": 1,
                "description": "Sort intervals by finish time. Select Job 1 [0, 2] (finishes earliest).",
                "array": ["[0, 2]", "[1, 4]", "[2, 5]", "[3, 7]", "[5, 8]"],
                "pointers": { "selected": 0 },
                "highlights": { "0": "sorted" },
                "variables": { "currentEnd": 2, "selectedCount": 1 },
                "invariants": "Greedy choice property: picking earliest finish leaves maximum remaining time"
            },
            {
                "step": 2,
                "description": "Inspect Job 2 [1, 4]: Start time 1 < currentEnd 2 -> Conflict! Reject Job 2.",
                "array": ["[0, 2]", "[1, 4] (Conflict)", "[2, 5]", "[3, 7]", "[5, 8]"],
                "pointers": { "curr": 1 },
                "highlights": { "0": "sorted", "1": "pivot" },
                "variables": { "currentEnd": 2, "action": "reject" },
                "invariants": "Non-overlapping invariant requires start_time >= previous end_time"
            },
            {
                "step": 3,
                "description": "Inspect Job 3 [2, 5]: Start time 2 >= currentEnd 2 -> Compatible! Select Job 3.",
                "array": ["[0, 2]", "[1, 4]", "[2, 5]", "[3, 7]", "[5, 8]"],
                "pointers": { "selected": 2 },
                "highlights": { "0": "sorted", "2": "sorted" },
                "variables": { "currentEnd": 5, "selectedCount": 2 },
                "invariants": "Update active end time boundary to 5"
            }
        ]
    },

    "Module_13_Backtracking_and_Constraint_Satisfaction": {
        "title": "4-Queens Constraint Satisfaction Backtracking",
        "algorithm": "Backtracking Search Tree with Pruning",
        "timeComplexity": "O(N!)",
        "spaceComplexity": "O(N)",
        "frames": [
            {
                "step": 1,
                "description": "Place Queen 0 at (Row 0, Col 1). Column 1 and diagonals marked attacked.",
                "array": ["Q at (0, 1)", "Empty Row 1", "Empty Row 2", "Empty Row 3"],
                "pointers": { "row": 0 },
                "highlights": { "0": "active" },
                "variables": { "cols": [1], "diags1": [1], "diags2": [-1] },
                "invariants": "No two queens share same row, column, or diagonal"
            },
            {
                "step": 2,
                "description": "Row 1: Col 0 attacked (diagonal), Col 1 attacked (column), Col 2 attacked (diagonal). Col 3 VALID! Place Queen 1 at (1, 3).",
                "array": ["Q at (0, 1)", "Q at (1, 3)", "Empty Row 2", "Empty Row 3"],
                "pointers": { "row": 1 },
                "highlights": { "0": "active", "1": "active" },
                "variables": { "cols": [1, 3], "row": 1 },
                "invariants": "Advance to next row once valid column placement confirmed"
            },
            {
                "step": 3,
                "description": "Row 2: Col 0 valid! Place Queen 2 at (2, 0). Row 3: Col 2 valid! Place Queen 3 at (3, 2). Complete solution found!",
                "array": ["Q at (0, 1)", "Q at (1, 3)", "Q at (2, 0)", "Q at (3, 2)"],
                "pointers": { "row": 3 },
                "highlights": { "0": "sorted", "1": "sorted", "2": "sorted", "3": "sorted" },
                "variables": { "solution": [1, 3, 0, 2], "complete": True },
                "invariants": "All 4 queens placed with zero mutually conflicting attack lines"
            }
        ]
    },

    "Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree": {
        "title": "Disjoint Set Union (Union by Rank & Path Compression)",
        "algorithm": "Union-Find DSU",
        "timeComplexity": "O(α(n)) amortized inverse Ackermann",
        "spaceComplexity": "O(n)",
        "frames": [
            {
                "step": 1,
                "description": "Initial forest: 5 singleton sets [0, 1, 2, 3, 4], each pointing to self.",
                "array": ["0->0", "1->1", "2->2", "3->3", "4->4"],
                "pointers": { "sets": 5 },
                "highlights": { "0": "active", "1": "active", "2": "active", "3": "active", "4": "active" },
                "variables": { "numComponents": 5, "ranks": [0, 0, 0, 0, 0] },
                "invariants": "Parent pointers establish partition components"
            },
            {
                "step": 2,
                "description": "Union(0, 1) and Union(2, 3): Roots merged by rank. Components reduce 5 -> 3.",
                "array": ["0->0", "1->0", "2->2", "3->2", "4->4"],
                "pointers": { "root0": 0, "root2": 2 },
                "highlights": { "0": "sorted", "1": "sorted", "2": "sorted", "3": "sorted" },
                "variables": { "numComponents": 3, "ranks": [1, 0, 1, 0, 0] },
                "invariants": "Lower rank tree becomes child of higher rank root to maintain shallow depth"
            },
            {
                "step": 3,
                "description": "Find(3) with Path Compression: node 3 updates parent pointer directly to root 0! Depth becomes 1.",
                "array": ["0->0", "1->0", "2->0", "3->0", "4->4"],
                "pointers": { "root": 0 },
                "highlights": { "0": "sorted", "1": "sorted", "2": "sorted", "3": "sorted" },
                "variables": { "findResult": 0, "compressed": True },
                "invariants": "Path compression flattens tree structure during traversal"
            }
        ]
    },

    "Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU": {
        "title": "Skip List Geometric Multi-Level Index Search",
        "algorithm": "Skip List Forward Traversal",
        "timeComplexity": "O(log n)",
        "spaceComplexity": "O(n)",
        "frames": [
            {
                "step": 1,
                "description": "Target is 17. Start at top Express Level 2. Next node is 10 (10 < 17). Advance to 10.",
                "array": ["L2: 0 -> 10 -> 25", "L1: 0 -> 10 -> 15 -> 20 -> 25", "L0: All nodes"],
                "pointers": { "level": 2, "curr": 10 },
                "highlights": { "0": "active", "1": "active" },
                "variables": { "level": 2, "currVal": 10, "target": 17 },
                "invariants": "Skip large spans of elements on high express lanes"
            },
            {
                "step": 2,
                "description": "At Node 10, next in L2 is 25 (25 > 17). Cannot advance in L2! Drop down to Level 1.",
                "array": ["L2: 0 -> 10 -> 25", "L1: 0 -> 10 -> 15 -> 20 -> 25", "L0: All nodes"],
                "pointers": { "level": 1, "curr": 10 },
                "highlights": { "1": "active" },
                "variables": { "level": 1, "currVal": 10, "action": "drop_level" },
                "invariants": "Drop one level down when next node exceeds target key"
            },
            {
                "step": 3,
                "description": "In L1: 10 -> 15 (15 < 17, advance). Next is 20 (20 > 17). Drop to L0: 15 -> 17 Match found!",
                "array": ["L2: 0 -> 10 -> 25", "L1: 0 -> 10 -> 15 -> 20 -> 25", "L0: 0..15 -> 17 -> 20"],
                "pointers": { "level": 0, "curr": 17 },
                "highlights": { "2": "sorted" },
                "variables": { "found": True, "target": 17, "comparisons": 5 },
                "invariants": "Search cost bounded by O(log n) expected steps with 1/2 geometric coin flips"
            }
        ]
    },

    "Module_16_String_Algorithms_and_Pattern_Matching": {
        "title": "KMP Pattern Matching Prefix Function (Pi Table)",
        "algorithm": "Knuth-Morris-Pratt Search",
        "timeComplexity": "O(n + m)",
        "spaceComplexity": "O(m)",
        "frames": [
            {
                "step": 1,
                "description": "Text: 'ABABDABACD', Pattern: 'ABAC'. Match 'A', 'B', 'A' (3 chars matched).",
                "array": ["A", "B", "A", "B", "D", "A", "B", "A", "C", "D"],
                "pointers": { "textIdx": 2, "patIdx": 2 },
                "highlights": { "0": "sorted", "1": "sorted", "2": "sorted" },
                "variables": { "matched": "ABA", "pi_table": [0, 0, 1, 0] },
                "invariants": "Prefix function pi[2] = 1 indicates prefix 'A' matches suffix 'A'"
            },
            {
                "step": 2,
                "description": "Mismatch at text[3] ('B') vs pat[3] ('C'). Fallback to patIdx = pi[2] = 1! Do NOT backtrack text pointer!",
                "array": ["A", "B", "A", "B", "D", "A", "B", "A", "C", "D"],
                "pointers": { "textIdx": 3, "patIdx": 1 },
                "highlights": { "3": "pivot" },
                "variables": { "textChar": "B", "patChar": "C", "fallbackIdx": 1 },
                "invariants": "KMP avoids rolling back text index, guaranteeing strict O(n) text scan"
            }
        ]
    },

    "Module_17_Network_Flow_and_Matching": {
        "title": "Dinic's Algorithm Level Graph BFS & Augmenting Path",
        "algorithm": "Dinic Maximum Flow",
        "timeComplexity": "O(V^2 * E)",
        "spaceComplexity": "O(V + E)",
        "frames": [
            {
                "step": 1,
                "description": "BFS builds Layered Graph: Source S (Layer 0), U & V (Layer 1), W & X (Layer 2), Sink T (Layer 3).",
                "array": ["S (L0)", "U (L1)", "V (L1)", "W (L2)", "X (L2)", "T (L3)"],
                "pointers": { "source": 0, "sink": 5 },
                "highlights": { "0": "sorted", "5": "pivot" },
                "variables": { "sinkLevel": 3, "layeredGraphBuilt": True },
                "invariants": "Residual edges are only admissible if level[v] == level[u] + 1"
            },
            {
                "step": 2,
                "description": "DFS pushes blocking flow along path S -> U -> W -> T: bottleneck capacity = 4.",
                "array": ["S: 4/10", "U: 4/10", "W: 4/4 (Saturated!)", "T: 4/10"],
                "pointers": { "bottleneck": 2 },
                "highlights": { "2": "pivot", "3": "sorted" },
                "variables": { "pushedFlow": 4, "totalFlow": 4 },
                "invariants": "Edge W->T is saturated, blocking further flow along this subpath"
            },
            {
                "step": 3,
                "description": "DFS pushes blocking flow along S -> U -> X -> T (flow 6) and S -> V -> X -> T (flow 4). Total max flow = 14!",
                "array": ["S: 14", "U: 10", "V: 4", "W: 4", "X: 10", "T: 14 (Max Flow)"],
                "pointers": { "sink": 5 },
                "highlights": { "0": "sorted", "5": "sorted" },
                "variables": { "maxFlow": 14, "iterations": 2 },
                "invariants": "Max-Flow Min-Cut Theorem: Total cut capacity == Max flow == 14"
            }
        ]
    }
}

def main():
    root = Path("02_Data_Structures_and_Algorithms")
    count = 0
    for mod_name, trace_data in MODULE_TRACES.items():
        mod_dir = root / mod_name
        if not mod_dir.is_dir():
            print(f"Skipping missing directory: {mod_dir}")
            continue
        trace_file = mod_dir / "trace.json"
        with open(trace_file, "w", encoding="utf-8") as f:
            json.dump(trace_data, f, indent=2)
        count += 1
        print(f"Generated {trace_file}")

    print(f"\nSuccessfully created {count} trace.json files in Course 02!")

if __name__ == '__main__':
    main()
