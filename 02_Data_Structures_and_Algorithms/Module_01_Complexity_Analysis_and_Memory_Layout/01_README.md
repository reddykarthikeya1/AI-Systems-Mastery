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

### Problem 1: Two Sum ([LeetCode 1](https://leetcode.com/problems/two-sum/)) — Easy

#### Brute Force: Pairwise Nested Search
Iterate through every pair $(i, j)$ where $i \neq j$ and check if $nums[i] + nums[j] == target$.
```python
def two_sum_brute(nums: list[int], target: int) -> list[int]:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```
- **Time Complexity**: $O(N^2)$ — $\\frac{N(N-1)}{2}$ comparisons. Hits TLE on large arrays ($N \ge 10^5$).
- **Space Complexity**: $O(1)$ — No extra memory allocated.

#### Optimized: One-Pass Hash Map
Store each visited value and its index. For each element $x$, check if $(target - x)$ exists in the hash map.
```python
def two_sum_optimal(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```
- **Time Complexity**: $O(N)$ — Single pass; $O(1)$ average hash table lookup.
- **Space Complexity**: $O(N)$ — Stores up to $N$ entries in the hash table.

---

### Problem 2: Majority Element ([LeetCode 169](https://leetcode.com/problems/majority-element/)) — Easy

#### Brute Force: Frequency Hash Map
Count frequencies of each element and return the one where $count > \\lfloor N/2 \\rfloor$.
```python
def majority_element_brute(nums: list[int]) -> int:
    counts: dict[int, int] = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
        if counts[x] > len(nums) // 2:
            return x
    return -1
```
- **Time**: $O(N)$, **Space**: $O(N)$ auxiliary memory.

#### Optimized: Boyer-Moore Voting Algorithm ($O(1)$ Space)
Maintain a `candidate` and a `count`. If `count == 0`, assign new candidate. Increment when equal, decrement otherwise.
```python
def majority_element_optimal(nums: list[int]) -> int:
    candidate = nums[0]
    count = 0
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
    return candidate
```
- **Time Complexity**: $O(N)$ — Exactly 1 linear pass.
- **Space Complexity**: $O(1)$ — Only two scalar variables.

---

### Problem 3: Missing Number ([LeetCode 268](https://leetcode.com/problems/missing-number/)) — Easy

#### Brute Force: Hash Set Lookup
```python
def missing_number_brute(nums: list[int]) -> int:
    seen = set(nums)
    for i in range(len(nums) + 1):
        if i not in seen:
            return i
    return -1
```
- **Time**: $O(N)$, **Space**: $O(N)$.

#### Optimized: XOR Bit Manipulation ($O(1)$ Space)
Exploit $X \\oplus X = 0$ and $X \\oplus 0 = X$. XOR all numbers in $[0, N]$ and all numbers in `nums`.
```python
def missing_number_optimal(nums: list[int]) -> int:
    missing = len(nums)
    for i, num in enumerate(nums):
        missing ^= i ^ num
    return missing
```
- **Time Complexity**: $O(N)$, **Space Complexity**: $O(1)$. No integer overflow hazard.

---

### Problem 4: Single Number ([LeetCode 136](https://leetcode.com/problems/single-number/)) — Easy

#### Brute Force: Frequency Hash Map
- **Time**: $O(N)$, **Space**: $O(N)$ auxiliary storage.

#### Optimized: XOR Cumulative Fold
```python
def single_number_optimal(nums: list[int]) -> int:
    res = 0
    for x in nums:
        res ^= x
    return res
```
- **Time Complexity**: $O(N)$, **Space Complexity**: $O(1)$.

---

### Problem 5: Power of Two ([LeetCode 231](https://leetcode.com/problems/power-of-two/)) — Easy

#### Brute Force: Iterative Division
Repeatedly divide by 2 while $n > 1$.
```python
def is_power_of_two_brute(n: int) -> bool:
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1
```
- **Time Complexity**: $O(\\log N)$.

#### Optimized: Bitwise Invariant ($O(1)$ Time)
A positive power of two has exactly one set bit in binary (e.g. $8 = 1000_2$, $7 = 0111_2$). Hence $n \\ \\& \\ (n - 1) == 0$.
```python
def is_power_of_two_optimal(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0
```
- **Time Complexity**: $O(1)$ — Single CPU machine instruction.
- **Space Complexity**: $O(1)$.

---

### Problem 6: Number of 1 Bits ([LeetCode 191](https://leetcode.com/problems/number-of-1-bits/)) — Easy

#### Brute Force: Check All 32 Bits
```python
def hamming_weight_brute(n: int) -> int:
    count = 0
    for _ in range(32):
        count += (n & 1)
        n >>= 1
    return count
```
- **Time**: $O(32) = O(1)$ fixed loop iterations.

#### Optimized: Brian Kernighan's Algorithm
$n \\ \\& \\ (n - 1)$ clears the least significant set bit in $O(1)$ steps. Iterates only as many times as there are 1-bits.
```python
def hamming_weight_optimal(n: int) -> int:
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count
```
- **Time Complexity**: $O(k)$ where $k$ is the number of set bits ($k \le 32$).
- **Space Complexity**: $O(1)$.

---

### Problem 7: Counting Bits ([LeetCode 338](https://leetcode.com/problems/counting-bits/)) — Easy

#### Brute Force: Count per Number
Call bit count for each number from $0$ to $N$.
- **Time Complexity**: $O(N \\log N)$.

#### Optimized: Bit Shift Dynamic Programming
$dp[i] = dp[i >> 1] + (i \\ \\& \\ 1)$.
```python
def count_bits_optimal(n: int) -> list[int]:
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```
- **Time Complexity**: $O(N)$ — Single pass.
- **Space Complexity**: $O(N)$ for output array.

---

### Problem 8: Reverse Bits ([LeetCode 190](https://leetcode.com/problems/reverse-bits/)) — Easy

#### Optimized: Bit Reversal Masking
```python
def reverse_bits_optimal(n: int) -> int:
    res = 0
    for i in range(32):
        bit = (n >> i) & 1
        res |= (bit << (31 - i))
    return res
```
- **Time Complexity**: $O(1)$ — Exactly 32 operations.
- **Space Complexity**: $O(1)$.

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