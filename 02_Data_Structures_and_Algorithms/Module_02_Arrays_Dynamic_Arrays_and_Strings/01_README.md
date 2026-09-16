# Module 02: Arrays, Dynamic Arrays & Strings (0 to 100 Mastery)

> **The Hardware Reality & Algorithmic Foundations of Sequential Data**

Arrays and strings are the bedrock of all computer software. From OS kernel buffers to transformer token sequences, every high-performance system begins with contiguous blocks of memory. In this module, you will master the hardware physics of memory caches, the mathematical proofs of dynamic array amortization, and the 4 fundamental array algorithmic patterns (Two Pointers, Sliding Window, Prefix Sum, In-Place Transformations) with exhaustive **Brute Force vs. Optimized** LeetCode breakdowns.

---

## Table of Contents
1. [Physical Hardware Memory Layout & Cache Physics](#1-physical-hardware-memory-layout--cache-physics)
2. [Dynamic Array Geometric Resizing & Amortization Proofs](#2-dynamic-array-geometric-resizing--amortization-proofs)
3. [CPython List & String Memory Internals (PEP 393)](#3-cpython-list--string-memory-internals-pep-393)
4. [The 4 Foundational Algorithmic Patterns](#4-the-4-foundational-algorithmic-patterns)
5. [The Master LeetCode Problem Suite (Brute Force vs. Optimized)](#5-the-master-leetcode-problem-suite-brute-force-vs-optimized)
   - [1. LeetCode 1: Two Sum](#problem-1-two-sum-leetcode-1--easy)
   - [2. LeetCode 121: Best Time to Buy and Sell Stock](#problem-2-best-time-to-buy-and-sell-stock-leetcode-121--easy)
   - [3. LeetCode 217: Contains Duplicate](#problem-3-contains-duplicate-leetcode-217--easy)
   - [4. LeetCode 238: Product of Array Except Self](#problem-4-product-of-array-except-self-leetcode-238--medium)
   - [5. LeetCode 53: Maximum Subarray (Kadane's Algorithm)](#problem-5-maximum-subarray-leetcode-53--medium)
   - [6. LeetCode 167: Two Sum II - Input Array Is Sorted](#problem-6-two-sum-ii---input-array-is-sorted-leetcode-167--medium)
   - [7. LeetCode 15: 3Sum](#problem-7-3sum-leetcode-15--medium)
   - [8. LeetCode 11: Container With Most Water](#problem-8-container-with-most-water-leetcode-11--medium)
   - [9. LeetCode 42: Trapping Rain Water](#problem-9-trapping-rain-water-leetcode-42--hard)
   - [10. LeetCode 3: Longest Substring Without Repeating Characters](#problem-10-longest-substring-without-repeating-characters-leetcode-3--medium)
   - [11. LeetCode 76: Minimum Window Substring](#problem-11-minimum-window-substring-leetcode-76--hard)
   - [12. LeetCode 560: Subarray Sum Equals K](#problem-12-subarray-sum-equals-k-leetcode-560--medium)
   - [13. LeetCode 56: Merge Intervals](#problem-13-merge-intervals-leetcode-56--medium)
   - [14. LeetCode 48: Rotate Image](#problem-14-rotate-image-leetcode-48--medium)
6. [Learning Path & Deliverables](#6-learning-path--deliverables)

---

## 1. Physical Hardware Memory Layout & Cache Physics

### Contiguous Allocation & Address Calculation
An array is a contiguous chunk of physical memory bytes. Because every element has a uniform byte size $S$, calculating the memory address of element $i$ requires a single CPU multiplication and addition in $O(1)$ time:

$$\text{Address}(A[i]) = \text{BaseAddress} + (i \times S)$$

```
RAM Addresses:  0x1000      0x1008      0x1010      0x1018      0x1020
Elements:     |  A[0]    |  A[1]    |  A[2]    |  A[3]    |  A[4]    |
Bytes:        | 8 bytes  | 8 bytes  | 8 bytes  | 8 bytes  | 8 bytes  |
```

### CPU Cache Hierarchy & Spatial Locality
Modern CPUs do not fetch single bytes from RAM; they fetch **Cache Lines (typically 64 bytes)** into high-speed L1/L2 caches.
- **Sequential Array Access**: Accessing `A[0]` pulls `A[0]` through `A[7]` into L1 cache immediately. Iterating through `A[1]` to `A[7]` produces near-instant **L1 Cache Hits** (latency ~1 ns).
- **Linked List Pointer Chasing**: Each node lives at an arbitrary heap address. Traversal causes frequent **L1/L2 Cache Misses**, forcing the CPU to stall for RAM fetch cycles (latency ~50-100 ns).
- **Architectural Takeaway**: An $O(N)$ contiguous array pass is frequently **10x to 50x faster in wall-clock time** than an $O(N)$ linked list traversal despite identical theoretical Big-O complexity!

---

## 2. Dynamic Array Geometric Resizing & Amortization Proofs

Static arrays have fixed capacity. Dynamic arrays (e.g., Python `list`, C++ `std::vector`, Java `ArrayList`) provide dynamic appending by managing an internal buffer with a growth factor $G$ (typically $1.5\times$ or $2\times$).

```
Step 1: Capacity = 2, Size = 2  ->  [ 10 | 20 ]
Step 2: Append 30 (Buffer Full!)
Step 3: Allocate new buffer (Capacity = 4)
Step 4: Copy elements [10, 20] -> [ 10 | 20 | 30 | _ ]  (Cost: 2 copies + 1 append)
```

### The Mathematical Proof of $O(1)$ Amortized Append

#### Why Linear Growth Fails ($+C$ increment)
If an array grows by a fixed increment $+C$ whenever full, after $N$ insertions it reallocates $N/C$ times. The total copying work is:

$$\sum_{k=1}^{N/C} kC = C \frac{(N/C)(N/C + 1)}{2} = O(N^2)$$

Dividing by $N$ insertions yields $O(N)$ cost per insertion. Linear resizing is a performance disaster.

#### Why Geometric Growth Succeeds ($	imes 2$ multiplier)
If capacity doubles ($2, 4, 8, 16 \dots 2^k$), the total number of reallocations for $N$ elements is $\log_2 N$. The total copying work is a geometric series:

$$\text{Total Copies} = 1 + 2 + 4 + 8 + \dots + \frac{N}{2} = \sum_{j=0}^{\log_2 N - 1} 2^j = N - 1 < N$$

The **Amortized Cost** per append operation is:

$$\text{Amortized Cost} = \frac{\text{Total Work}}{\text{Total Operations}} = \frac{N \text{ (raw appends)} + N \text{ (copies)}}{N} = O(1)$$

---

## 3. CPython List & String Memory Internals (PEP 393)

### CPython `PyListObject` Implementation
In Python, a `list` is a contiguous array of pointer references (`PyObject*`). CPython uses a custom growth formula in `listobject.c`:

$$\text{new\_allocated} = \text{newsize} + (\text{newsize} \gg 3) + (3 \text{ if newsize } < 9 \text{ else } 6)$$

This produces the exact over-allocation capacity progression:
`0 -> 4 -> 8 -> 16 -> 24 -> 32 -> 40 -> 52 -> 64 -> 76 -> 92 -> 112...`

### Python String Immutability & PEP 393 Flexible Representation
Python strings are immutable sequences of unicode characters.
- **Why Immutability?**: Allows strings to be safely used as dictionary keys (hash value cached once at creation) and enables thread-safe sharing without locking.
- **The String Concatenation Trap**: Repeatedly appending strings in a loop via `s += char` creates a new string object every iteration, copying all previous characters:

$$1 + 2 + 3 + \dots + N = O(N^2) \text{ time!}$$

**Correct Production Idiom**: Accumulate in a list and use `''.join(buffer)` in $O(N)$ time.

---

## 4. The 4 Foundational Algorithmic Patterns

```
PATTERN 1: TWO POINTERS (CONVERGING)
[ L -------->                 <-------- R ]
Best for: Sorted arrays, pair sum targets, palindromes, container heights.

PATTERN 2: SLIDING WINDOW (DYNAMIC EXPAND / CONTRACT)
[       L ===== R ] ------------>
Best for: Substring problems, contiguous subarray sums, max/min subsegment constraints.

PATTERN 3: PREFIX SUM & RUNNING AGGREGATES
Original:   [ a0,   a1,        a2,        a3 ]
PrefixSum:  [ 0,    a0,     a0+a1,  a0+a1+a2 ]
Best for: Subarray sum queries in O(1), subarray sum equals K via hash maps.

PATTERN 4: IN-PLACE ARRAY CYCLING
Swap elements in-place to achieve O(1) auxiliary space (e.g. reverse, matrix transpose).
```

---

## 5. The Master LeetCode Problem Suite (Brute Force vs. Optimized)

---

### Problem 1: Two Sum ([LeetCode 1](https://leetcode.com/problems/two-sum/)) — Easy

> **Problem Statement**: Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. Each input has exactly one solution, and you cannot use the same element twice.

#### 1. Intuition & Mental Model
We are looking for pairs $(a, b)$ such that $a + b = \text{target}$. For any element $x$, the required value is $\text{complement} = \text{target} - x$. The question is how fast we can check if the complement exists.

#### 2. Brute Force Approach
Compare every possible pair of elements with two nested loops.

```python
def two_sum_brute(nums: list[int], target: int) -> list[int]:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```
- **Time Complexity**: $O(N^2)$ — Tests $N(N-1)/2$ pairs.
- **Space Complexity**: $O(1)$ — No auxiliary data structures.
- **Why It Fails**: For $N = 10^5$, $N^2 = 10^{10}$ operations, exceeding the 1-second execution limit (~$10^8$ ops) and triggering **Time Limit Exceeded (TLE)**.

#### 3. Optimized Approach (One-Pass Hash Map)
As we traverse the array, maintain a hash table mapping `value -> index`. For each number, query if `target - num` already exists in the map.

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
- **Time Complexity**: $O(N)$ — Single pass; hash map lookups and insertions are $O(1)$ on average.
- **Space Complexity**: $O(N)$ — Stores up to $N$ elements in the hash map.
- **Key Takeaway**: Trade space for time. Convert a search query from $O(N)$ to $O(1)$ using a hash table.

---

### Problem 2: Best Time to Buy and Sell Stock ([LeetCode 121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)) — Easy

> **Problem Statement**: You are given an array `prices` where `prices[i]` is the price of a given stock on the $i$-th day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit.

#### 1. Brute Force Approach
Test every pair $(i, j)$ where $j > i$ and find the maximum difference `prices[j] - prices[i]`.

```python
def max_profit_brute(prices: list[int]) -> int:
    max_prof = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            max_prof = max(max_prof, prices[j] - prices[i])
    return max_prof
```
- **Time Complexity**: $O(N^2)$ — Quadratic pair evaluation.
- **Space Complexity**: $O(1)$.

#### 2. Optimized Approach (Single-Pass Running Minimum)
To maximize profit when selling on day $i$, we must have bought at the minimum price seen on days $0$ through $i-1$. Track `min_price` dynamically.

```python
def max_profit_optimal(prices: list[int]) -> int:
    min_price = float('inf')
    max_prof = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_prof:
            max_prof = price - min_price
    return max_prof
```
- **Time Complexity**: $O(N)$ — Single pass through the prices array.
- **Space Complexity**: $O(1)$ — Only two scalar variables.
- **Key Takeaway**: Maintain a rolling invariant (running minimum prefix).

---

### Problem 3: Contains Duplicate ([LeetCode 217](https://leetcode.com/problems/contains-duplicate/)) — Easy

> **Problem Statement**: Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

#### 1. Brute Force Approach
Compare every pair in $O(N^2)$ time, or sort the array in $O(N \log N)$ time and scan adjacent elements.

#### 2. Optimized Approach (Hash Set)
```python
def contains_duplicate_optimal(nums: list[int]) -> bool:
    seen: set[int] = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```
- **Time Complexity**: $O(N)$ — Early exit on first duplicate.
- **Space Complexity**: $O(N)$ — Stores unique elements in a hash set.

---

### Problem 4: Product of Array Except Self ([LeetCode 238](https://leetcode.com/problems/product-of-array-except-self/)) — Medium

> **Problem Statement**: Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`. You must write an algorithm that runs in $O(N)$ time and without using the division operation.

#### 1. Intuition & Mental Model
For any index $i$, the total product excluding `nums[i]` is:

$$\text{answer}[i] = \prod_{j < i} \text{nums}[j] \times \prod_{j > i} \text{nums}[j] = \text{prefix\_product}[i] \times \text{suffix\_product}[i]$$

#### 2. Brute Force Approach
For each index $i$, run a loop over all other $j \ne i$ multiplying values.
- **Time Complexity**: $O(N^2)$.
- **Space Complexity**: $O(1)$ auxiliary.

#### 3. Optimized Approach ($O(N)$ Time, $O(1)$ Extra Space)
Compute prefix products directly into the result array, then sweep backwards with a running suffix accumulator.

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n
    
    # Pass 1: res[i] contains product of elements to the left of i
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
        
    # Pass 2: Multiply by running product of elements to the right of i
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
        
    return res
```
- **Time Complexity**: $O(N)$ — Two sequential linear passes.
- **Space Complexity**: $O(1)$ — The output array does not count as extra space per problem specifications.
- **Key Takeaway**: Prefix and suffix product decomposition eliminates division entirely.

---

### Problem 5: Maximum Subarray ([LeetCode 53](https://leetcode.com/problems/maximum-subarray/)) — Medium

> **Problem Statement**: Given an integer array `nums`, find the subarray with the largest sum, and return its sum.

#### 1. Intuition (Kadane's Algorithm)
At any element `nums[i]`, we decide whether to add `nums[i]` to our current running subarray, or discard the previous subarray and start fresh at `nums[i]`. If our previous running sum is negative, it can only drag down future sums.

$$S[i] = \max(\text{nums}[i], S[i-1] + \text{nums}[i])$$

#### 2. Brute Force Approach
Test all subarrays $[i, j]$:

```python
def max_sub_array_brute(nums: list[int]) -> int:
    max_sum = float('-inf')
    n = len(nums)
    for i in range(n):
        curr_sum = 0
        for j in range(i, n):
            curr_sum += nums[j]
            max_sum = max(max_sum, curr_sum)
    return max_sum
```
- **Time Complexity**: $O(N^2)$.
- **Space Complexity**: $O(1)$.

#### 3. Optimized Approach (Kadane's Algorithm in $O(N)$)
```python
def max_sub_array_optimal(nums: list[int]) -> int:
    current_sum = nums[0]
    max_sum = nums[0]
    
    for x in nums[1:]:
        # Either extend the existing subarray or start a new one from x
        current_sum = max(x, current_sum + x)
        max_sum = max(max_sum, current_sum)
        
    return max_sum
```
- **Time Complexity**: $O(N)$ — Single pass over array.
- **Space Complexity**: $O(1)$ — Only two scalar variables.
- **Key Takeaway**: Local optimal choice leads to global maximum for contiguous subarrays.

---

### Problem 6: Two Sum II - Input Array Is Sorted ([LeetCode 167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)) — Medium

> **Problem Statement**: Given a 1-indexed sorted array of integers `numbers`, find two numbers such that they add up to a specific `target` number. Must use $O(1)$ extra memory.

#### 1. Intuition & Two Pointers Proof
Place pointer `left = 0` and pointer `right = N - 1`.
- If `numbers[left] + numbers[right] == target`: Found!
- If `sum < target`: Because the array is sorted, increasing `left` is the *only* move that can increase the sum.
- If `sum > target`: Decreasing `right` is the *only* move that can decrease the sum.
This guarantees that no valid pair is ever skipped.

```python
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        curr = numbers[left] + numbers[right]
        if curr == target:
            return [left + 1, right + 1] # 1-indexed
        elif curr < target:
            left += 1
        else:
            right -= 1
    return []
```
- **Time Complexity**: $O(N)$ — Each step shrinks search space by 1.
- **Space Complexity**: $O(1)$ — No auxiliary memory.

---

### Problem 7: 3Sum ([LeetCode 15](https://leetcode.com/problems/3sum/)) — Medium

> **Problem Statement**: Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that $i \ne j, i \ne k, j \ne k$, and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.

#### 1. Brute Force Approach
Three nested loops testing all triplets: $O(N^3)$ time + hash set to filter duplicates. TLEs instantly.

#### 2. Optimized Approach (Sort + Two Pointers)
Sort the array first in $O(N \log N)$. For each element `nums[i]`, solve the Two Sum II problem for `target = -nums[i]` using two pointers on the remainder of the array. Skip identical elements to prevent duplicate triplets.

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    n = len(nums)
    
    for i in range(n - 2):
        # Optimization: If the smallest number > 0, three positives cannot sum to 0
        if nums[i] > 0:
            break
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                # Skip duplicate second and third elements
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
                
    return res
```
- **Time Complexity**: $O(N^2)$ — Sorting is $O(N \log N)$; outer loop runs $N$ times, each executing an $O(N)$ two-pointer sweep.
- **Space Complexity**: $O(1)$ or $O(N)$ depending on sorting implementation.

---

### Problem 8: Container With Most Water ([LeetCode 11](https://leetcode.com/problems/container-with-most-water/)) — Medium

> **Problem Statement**: Given an integer array `height` of length $n$, there are $n$ vertical lines drawn. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.

#### 1. Intuition & Greedy Two Pointers
The water volume bounded by lines $L$ and $R$ is:

$$\text{Area} = (R - L) \times \min(\text{height}[L], \text{height}[R])$$

To maximize area, start at the maximum possible width (`left = 0, right = n - 1`). The height of the container is bottlenecked by the **shorter line**. Moving the taller line inward can only decrease width without any chance of increasing the bottleneck height. Therefore, the **only move that could potentially yield a larger area is advancing the shorter line**.

```python
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        # Advance the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
            
    return max_water
```
- **Time Complexity**: $O(N)$ — Pointers meet in at most $N$ iterations.
- **Space Complexity**: $O(1)$.

---

### Problem 9: Trapping Rain Water ([LeetCode 42](https://leetcode.com/problems/trapping-rain-water/)) — Hard

> **Problem Statement**: Given $n$ non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

#### 1. Intuition
Water trapped above bar $i$ is determined by the minimum of the highest wall to its left and the highest wall to its right, minus its own height:

$$\text{Water}[i] = \max(0, \min(\text{left\_max}[i], \text{right\_max}[i]) - \text{height}[i])$$

#### 2. Intermediate Approach (Prefix Max & Suffix Max Arrays)
Precompute `left_max` and `right_max` arrays in $O(N)$ time and $O(N)$ space.

#### 3. Optimal Approach (Two Pointers in $O(1)$ Space)
Maintain `left_max` and `right_max`. Whichever side has the smaller bound bottlenecks the water level, allowing us to compute trapped water on that side immediately and advance that pointer.

```python
def trap_water(height: list[int]) -> int:
    if not height:
        return 0
        
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            
    return water
```
- **Time Complexity**: $O(N)$ — Single pass.
- **Space Complexity**: $O(1)$ — Zero auxiliary arrays.

---

### Problem 10: Longest Substring Without Repeating Characters ([LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/)) — Medium

> **Problem Statement**: Given a string `s`, find the length of the longest substring without duplicate characters.

#### 1. Intuition & Dynamic Sliding Window
Maintain a sliding window $[L, R]$. As $R$ expands, if `s[R]` was previously seen inside our current window (at index `prev_idx >= L`), jump $L$ directly to `prev_idx + 1` to restore the unique characters invariant in $O(1)$ operations.

```python
def length_of_longest_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    max_len = 0
    
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
            
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)
        
    return max_len
```
- **Time Complexity**: $O(N)$ — Right pointer sweeps once from $0$ to $N-1$.
- **Space Complexity**: $O(\min(N, \Sigma))$ — Hash map of size at most the alphabet size $\Sigma$ (e.g. 128 for ASCII).

---

### Problem 11: Minimum Window Substring ([LeetCode 76](https://leetcode.com/problems/minimum-window-substring/)) — Hard

> **Problem Statement**: Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return `""`.

#### 1. Intuition
Use a variable sliding window with two frequency maps: `target_counts` and `window_counts`. Track `have` (number of unique characters meeting target count) vs. `need` (total distinct characters in `t`).
1. Expand `right` until `have == need`.
2. Once valid, record window length and shrink `left` as much as possible while maintaining `have == need`.
3. Repeat until end of string.

```python
from collections import Counter

def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
        
    target_counts = Counter(t)
    window_counts: dict[str, int] = {}
    
    have, need = 0, len(target_counts)
    res_len = float('inf')
    res_indices = (-1, -1)
    
    left = 0
    for right, char in enumerate(s):
        window_counts[char] = window_counts.get(char, 0) + 1
        if char in target_counts and window_counts[char] == target_counts[char]:
            have += 1
            
        while have == need:
            # Update best window
            window_len = right - left + 1
            if window_len < res_len:
                res_len = window_len
                res_indices = (left, right)
                
            # Pop left character from window
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in target_counts and window_counts[left_char] < target_counts[left_char]:
                have -= 1
            left += 1
            
    l, r = res_indices
    return s[l : r + 1] if res_len != float('inf') else ""
```
- **Time Complexity**: $O(|S| + |T|)$ — Each character in $S$ is visited at most twice (once by $R$, once by $L$).
- **Space Complexity**: $O(|S| + |T|)$ — Frequency hash maps.

---

### Problem 12: Subarray Sum Equals K ([LeetCode 560](https://leetcode.com/problems/subarray-sum-equals-k/)) — Medium

> **Problem Statement**: Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.

#### 1. Intuition & Prefix Sum Identity
A subarray sum from $i$ to $j$ is given by:

$$\text{Sum}(i, j) = \text{PrefixSum}[j] - \text{PrefixSum}[i - 1]$$

Setting $\text{Sum}(i, j) = k$ yields:

$$\text{PrefixSum}[i - 1] = \text{PrefixSum}[j] - k$$

As we iterate, maintain a hash map of `prefix_sum -> frequency`. For each running prefix sum $P$, add `map[P - k]` to our total count!

```python
def subarray_sum(nums: list[int], k: int) -> int:
    prefix_counts = {0: 1} # Base case: empty prefix has sum 0
    current_sum = 0
    total_count = 0
    
    for num in nums:
        current_sum += num
        # How many prefixes have sum (current_sum - k)?
        total_count += prefix_counts.get(current_sum - k, 0)
        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1
        
    return total_count
```
- **Time Complexity**: $O(N)$ — Single linear pass.
- **Space Complexity**: $O(N)$ — Prefix sum frequency hash map.
- **Crucial Distinction**: Sliding window does NOT work on this problem when negative numbers are present because the sum is not monotonic! Prefix sum with hash map works for all integers.

---

### Problem 13: Merge Intervals ([LeetCode 56](https://leetcode.com/problems/merge-intervals/)) — Medium

> **Problem Statement**: Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])
    merged: list[list[int]] = []
    
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            # No overlap, append directly
            merged.append(interval)
        else:
            # Overlap exists, expand end boundary of previous interval
            merged[-1][1] = max(merged[-1][1], interval[1])
            
    return merged
```
- **Time Complexity**: $O(N \log N)$ — Dominated by interval start time sorting.
- **Space Complexity**: $O(N)$ — Output list.

---

### Problem 14: Rotate Image ([LeetCode 48](https://leetcode.com/problems/rotate-image/)) — Medium

> **Problem Statement**: You are given an $n \times n$ 2D matrix representing an image, rotate the image by 90 degrees (clockwise) **in-place** (without allocating another 2D matrix).

#### 1. In-Place Transposition Geometric Decomposition
A 90-degree clockwise rotation is mathematically equivalent to two simple in-place operations:
1. **Transpose the matrix** (reflect along main diagonal: swap `matrix[i][j]` with `matrix[j][i]`).
2. **Reverse each row** (reflect horizontally: reverse row `matrix[i]`).

```python
def rotate_matrix(matrix: list[list[int]]) -> None:
    n = len(matrix)
    
    # Step 1: Transpose matrix in-place
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            
    # Step 2: Reverse each row in-place
    for i in range(n):
        matrix[i].reverse()
```
- **Time Complexity**: $O(N^2)$ — Visits each cell twice.
- **Space Complexity**: $O(1)$ — Modifies matrix strictly in-place.

---

## 6. Learning Path & Deliverables

1. **Beginner Friendly Playground**: Read [02_W3_BEGINNER_PLAYGROUND.md](02_W3_BEGINNER_PLAYGROUND.md) for ultra-gentle intuitions.\n2. **Interactive CLI Playground**: Run [03_try_it_yourself.py](03_try_it_yourself.py) in your terminal.\n3. **Interactive Notebook**: Open [00_interactive_arrays_dynamic_arrays_and_strings.ipynb](00_interactive_arrays_dynamic_arrays_and_strings.ipynb) for visual memory and algorithmic execution.
3. **Executable Demos**: Run [05_two_pointers_and_sliding_window_demos.py](05_two_pointers_and_sliding_window_demos.py) and [06_prefix_sum_and_kadane_demos.py](06_prefix_sum_and_kadane_demos.py).
4. **Build Reference Project**: Read the [07_PROJECT_GUIDE.md](07_PROJECT_GUIDE.md) and implement `dynamic_array_engine.py`.
5. **Self-Assessment**: Test your mastery with [08_SELF_ASSESSMENT_AND_CHALLENGES.md](08_SELF_ASSESSMENT_AND_CHALLENGES.md).
6. **Edge Cases**: Guard against production traps in [09_TROUBLESHOOTING_AND_EDGE_CASES.md](09_TROUBLESHOOTING_AND_EDGE_CASES.md).

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

### 2. Work the problem bank — 8 problems

```bash
cd problems
python -m pytest tests -q                    # all of this module's problems
python -m pytest tests -q -k p03             # just problem 3
```

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [Two Sum](problems/p01_two_sum.py) | Hash map complement | Easy | `Time O(n), Space O(n)` |
| 02 | [Maximum Sum Of A Fixed-Size Window](problems/p02_max_window_sum.py) | Sliding window (fixed) | Easy | `Time O(n), Space O(1)` |
| 03 | [Longest Substring With At Most K Distinct Characters](problems/p03_longest_k_distinct.py) | Sliding window (variable) | Medium | `Time O(n), Space O(k)` |
| 04 | [Count Subarrays Summing To K](problems/p04_subarray_sum_k.py) | Prefix sums + hash map | Medium | `Time O(n), Space O(n)` |
| 05 | [Product Of Array Except Self](problems/p05_product_except_self.py) | Prefix/suffix products | Medium | `Time O(n), Space O(1) beyond the output` |
| 06 | [Least Ship Capacity To Deliver In D Days](problems/p06_min_ship_capacity.py) | Binary search on the answer | Medium | `Time O(n log(sum)), Space O(1)` |
| 07 | [Three Sum](problems/p07_three_sum.py) | Sorting + two pointers | Medium | `Time O(n^2), Space O(1) beyond the output` |
| 08 | [Longest Palindromic Substring](problems/p08_longest_palindrome.py) | Expand around centre | Medium | `Time O(n^2), Space O(1)` |

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Every reference solution in `problems/solutions/` is cross-checked against
a brute force or a second implementation, so the answers are verified rather
than asserted.

### 3. Work the debug lab

```bash
cd debug_lab
python broken_array_toolkit.py
echo "exit=$?"
```

It exits 0 and prints wrong answers. Read [`SYMPTOMS.md`](debug_lab/SYMPTOMS.md),
write a diagnosis for each, and only then open `ANSWERS.md`. The diagnostic
reasoning is the transferable skill; reading the answer first skips it.

---

## ✅ You have mastered this module when you can…

1. Choose between two pointers, a sliding window, prefix sums and binary search on the answer from the constraints alone.
2. Explain why a sliding window is invalid for 'sum equals k' with negative numbers, and what replaces it.
3. Recognise 'minimise the maximum' as binary search on the answer, and write the monotone feasibility predicate.
4. Write a variable-size window whose shrink loop deletes zero-count keys, and say what breaks without the delete.

Each of these is something you **do**, not something you know. If you cannot do
one without reference, that is the section to revisit — not the whole module.

---

## 🧭 Navigation

- [Pattern Recognition Guide](../PATTERN_RECOGNITION_GUIDE.md) — how to attack a problem you have never seen
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md)
- [Problem bank](problems/README.md) · [Debug lab](debug_lab/SYMPTOMS.md)
