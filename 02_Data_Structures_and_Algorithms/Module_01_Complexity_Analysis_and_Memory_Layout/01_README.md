# Module 01: Complexity Analysis & Memory Layout (0 to 100 Mastery)

> **Asymptotic Bounds, CPU Cache Lines, RAM Architecture & Bit-Level Complexity**

Understanding algorithmic efficiency requires looking beneath high-level abstractions into hardware memory hierarchies and bit-level arithmetic. In this module, you master Big-O, Big-$\\Omega$, Big-$\\Theta$ mathematical proofs, recursion tree master theorems, CPU spatial/temporal locality, and amortized time bounds.

---


## Memory Hierarchy & Cache Locality Architecture

```mermaid
flowchart TD
    subgraph CPU["CPU Die"]
        subgraph Core["CPU Execution Core"]
            Reg["Registers<br/>(~1 KB, 0.5 ns)"]
        end
        L1["L1 Data Cache<br/>(32 KB, 1.0 ns, 4 cycles)<br/>64-Byte Line"]
        L2["L2 Cache<br/>(512 KB, 3.5 ns, 14 cycles)<br/>64-Byte Line"]
    end
    L3["L3 Shared Cache<br/>(32 MB, 12 ns, 50 cycles)<br/>64-Byte Line"]
    DRAM["Main Memory (DRAM)<br/>(64 GB, 60-100 ns, 200+ cycles)"]
    SSD["NVMe SSD Storage<br/>(2 TB, 10-50 µs, 50,000+ cycles)"]

    Reg <-->|Register Spill/Fill| L1
    L1 <-->|Cache Hit / Miss Line Fill| L2
    L2 <-->|Cross-Core Bus Snooping| L3
    L3 <-->|DDR5 Bus Transaction (64B)| DRAM
    DRAM <-->|PCIe Gen5 DMA Page Fault (4KB)| SSD

    classDef fast fill:#059669,stroke:#047857,color:#fff;
    classDef mid fill:#0284c7,stroke:#0369a1,color:#fff;
    classDef slow fill:#d97706,stroke:#b45309,color:#fff;
    classDef disc fill:#dc2626,stroke:#b91c1c,color:#fff;
    class Reg,L1 fast;
    class L2,L3 mid;
    class DRAM slow;
    class SSD disc;
```

---

## 1. Hardware Reality: CPU Caches vs RAM

```
[ CPU Registers: < 1 ns, ~1 KB ]
       |
[ L1 Cache: ~1 ns, 64 KB ]
       |
[ L2 Cache: ~4 ns, 512 KB ]
       |
[ L3 Cache: ~10 ns, 16 MB ]
       |
[ Main Memory (DRAM): ~50-100 ns, 16-64 GB ]
```

When iterating over an array, the CPU pre-fetches a **64-byte cache line** containing adjacent elements. A linked list, by contrast, causes CPU cache misses on nearly every pointer dereference.

---

## 2. Canonical LeetCode Problem Breakdowns (Brute Force vs. Optimized)

This section walks through the **6 canonical LeetCode challenges** curated for this module.
Each problem is analyzed from brute force intuition to the optimal invariant-driven solution, along with the critical edge cases to guard against in production.

### Problem 1: Binary Search ([LeetCode #704](https://leetcode.com/problems/binary-search/)) — Easy

> **Pattern**: `Two Pointers / Divide and Conquer` | **Target Time**: $O(\log N)$ | **Target Space**: $O(1)

#### Problem Specification
Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.

You must write an algorithm with $O(\log n)$ runtime complexity.

### Constraints
- $1 \le 	ext{nums.length} \le 10^4$
- $-10^4 < 	ext{nums}[i], 	ext{target} < 10^4$
- All integers in `nums` are unique.
- `nums` is sorted in ascending order.

#### Algorithmic Invariants & Optimal Derivation
Standard binary search with two pointers (left and right). At each step, compute mid to halve the search interval, achieving logarithmic $O(\log N)$ time and $O(1)$ auxiliary space.

```python
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 2: Search in Rotated Sorted Array ([LeetCode #33](https://leetcode.com/problems/search-in-rotated-sorted-array/)) — Medium

> **Pattern**: `Modified Binary Search` | **Target Time**: $O(\log N)$ | **Target Space**: $O(1)

#### Problem Specification
There is an integer array `nums` sorted in ascending order (with distinct values). Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index.

Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with $O(\log n)$ runtime complexity.

#### Algorithmic Invariants & Optimal Derivation
At least one half of the rotated array is always strictly sorted. We identify which half is sorted by comparing nums[left] with nums[mid], then check if target lies within that sorted range.

```python
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 3: Find Minimum in Rotated Sorted Array ([LeetCode #153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)) — Medium

> **Pattern**: `Inflection Point Binary Search` | **Target Time**: $O(\log N)$ | **Target Space**: $O(1)

#### Problem Specification
Suppose an array of length `n` sorted in ascending order is rotated between 1 and `n` times.
Given the sorted rotated array `nums` of unique elements, return the minimum element of this array.

You must write an algorithm that runs in $O(\log n)$ time.

#### Algorithmic Invariants & Optimal Derivation
Compare nums[mid] to nums[right]. If nums[mid] > nums[right], the minimum must be in the right subarray (excluding mid). Otherwise, it is in the left subarray including mid.

```python
class Solution:
    def findMin(self, nums: list[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        return nums[left]
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 4: Search a 2D Matrix ([LeetCode #74](https://leetcode.com/problems/search-a-2d-matrix/)) — Medium

> **Pattern**: `2D Flattened Binary Search` | **Target Time**: $O(\log(M 	imes N))$ | **Target Space**: $O(1)

#### Problem Specification
You are given an `m x n` integer matrix `matrix` with the following two properties:
1. Each row is sorted in non-decreasing order.
2. The first integer of each row is greater than the last integer of the previous row.

Given an integer `target`, return `true` if `target` is in `matrix` or `false` otherwise.
You must write a solution in $O(\log(m \cdot n))$ time.

#### Algorithmic Invariants & Optimal Derivation
Treat the M x N matrix as a single flattened 1D array of length M*N. Any 1D index `idx` maps directly to 2D coordinates via row = idx // N and col = idx % N.

```python
class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        m, n = len(matrix), len(matrix[0])
        left, right = 0, m * n - 1
        while left <= right:
            mid = (left + right) // 2
            val = matrix[mid // n][mid % n]
            if val == target:
                return True
            elif val < target:
                left = mid + 1
            else:
                right = mid - 1
        return False
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 5: First Bad Version ([LeetCode #278](https://leetcode.com/problems/first-bad-version/)) — Easy

> **Pattern**: `Lower Bound Predicate Binary Search` | **Target Time**: $O(\log N)$ | **Target Space**: $O(1)

#### Problem Specification
Suppose you have `n` versions `[1, 2, ..., n]` and you want to find out the first bad one, which causes all the following ones to be bad.

You are given an API `isBadVersion(version)` which returns whether `version` is bad. Implement a function to find the first bad version with minimum API calls.

#### Algorithmic Invariants & Optimal Derivation
Binary search on monotonic predicate: if `isBadVersion(mid)` is true, the first bad version is at or to the left of `mid` (right = mid). Otherwise it is strictly to the right (left = mid + 1).

```python
class Solution:
    def firstBadVersion(self, n: int, isBadVersion) -> int:
        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if isBadVersion(mid):
                right = mid
            else:
                left = mid + 1
        return left
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 6: Koko Eating Bananas ([LeetCode #875](https://leetcode.com/problems/koko-eating-bananas/)) — Medium

> **Pattern**: `Binary Search on Answer Space` | **Target Time**: $O(N \log(\max(P)))$ | **Target Space**: $O(1)

#### Problem Specification
Koko loves to eat bananas. There are `n` piles of bananas, the `i-th` pile has `piles[i]` bananas. The guards will come back in `h` hours.

Koko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile and eats `k` bananas from it. If the pile has less than `k` bananas, she eats all of them and will not eat any more bananas during this hour.

Return the minimum integer `k` such that she can eat all the bananas within `h` hours.

#### Algorithmic Invariants & Optimal Derivation
Search space is the speed k from 1 to max(piles). The feasibility function `sum(ceil(p/k)) <= h` is monotonic: if speed k works, all speeds > k also work. We use binary search to locate the minimum feasible speed.

```python
class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        import math
        left, right = 1, max(piles)
        ans = right
        while left <= right:
            mid = (left + right) // 2
            hours = sum(math.ceil(p / mid) for p in piles)
            if hours <= h:
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
        return ans
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---


## 3. Asymptotic Cheat Sheet

| Notation | Mathematical Definition | Intuition |
| :--- | :--- | :--- |
| **Big-O** $O(g(N))$ | $f(N) \le c \cdot g(N)$ for all $N \ge N_0$ | Upper bound (worst case guarantee) |
| **Big-$\\Omega$** $\\Omega(g(N))$ | $f(N) \ge c \cdot g(N)$ for all $N \ge N_0$ | Lower bound (best case limit) |
| **Big-$\\Theta$** $\\Theta(g(N))$ | $c_1 g(N) \le f(N) \le c_2 g(N)$ | Tight bound (exact asymptotic growth) |

---

## 4. Hands-On Project & Test Suite

Verify your profiling and complexity verification engines:
- Starter Template: [`starter/memory_benchmarker.py`](starter/memory_benchmarker.py)
- Production Solution: [`project_solution/memory_benchmarker.py`](project_solution/memory_benchmarker.py)
- Pytest Suite: [`project_solution/test_memory_benchmarker.py`](project_solution/test_memory_benchmarker.py)

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

### 2. Work the problem bank — 6 problems

```bash
cd problems
python -m pytest tests -q                    # all of this module's problems
python -m pytest tests -q -k p03             # just problem 3
```

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [Classify Empirical Growth Rate](problems/p01_classify_growth.py) | Complexity analysis | Easy | `Time O(k), Space O(k) for k measurements` |
| 02 | [Total Copies Under Geometric Growth](problems/p02_amortized_copies.py) | Amortized analysis | Medium | `Time O(log n), Space O(1)` |
| 03 | [Worst-Case Binary Search Comparisons](problems/p03_binary_search_steps.py) | Complexity analysis | Easy | `Time O(1), Space O(1)` |
| 04 | [Count Distinct Pair Iterations](problems/p04_pair_iterations.py) | Complexity analysis | Easy | `Time O(1), Space O(1)` |
| 05 | [Does This Complexity Fit The Constraint?](problems/p05_fits_budget.py) | Complexity analysis | Medium | `Time O(1) amortised, Space O(1)` |
| 06 | [Row-Major Memory Layout](problems/p06_row_major.py) | Memory layout | Easy | `Time O(1), Space O(1)` |

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Every reference solution in `problems/solutions/` is cross-checked against
a brute force or a second implementation, so the answers are verified rather
than asserted.

### 3. Work the debug lab

```bash
cd debug_lab
python broken_complexity_report.py
echo "exit=$?"
```

It exits 0 and prints wrong answers. Read [`SYMPTOMS.md`](debug_lab/SYMPTOMS.md),
write a diagnosis for each, and only then open `ANSWERS.md`. The diagnostic
reasoning is the transferable skill; reading the answer first skips it.

---

## ✅ You have mastered this module when you can…

1. State the complexity budget implied by any constraint on n, from n <= 10 to n <= 10**9, without looking it up.
2. Derive the total element copies for n appends under geometric growth, and show the per-append average is bounded.
3. Explain why `bit_length()` beats `math.log2` for an exact integer answer above 2**53.
4. Read a problem's constraints and name the techniques that fit the budget before reading the statement.

Each of these is something you **do**, not something you know. If you cannot do
one without reference, that is the section to revisit — not the whole module.

---

## 🧭 Navigation

- [Pattern Recognition Guide](../PATTERN_RECOGNITION_GUIDE.md) — how to attack a problem you have never seen
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md)
- [Problem bank](problems/README.md) · [Debug lab](debug_lab/SYMPTOMS.md)