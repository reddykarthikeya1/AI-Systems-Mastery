# DSA Playbook Chapter 3: The Complete Core 75 Mastery Walkthroughs

> **Core Learning Objective:** Master every single archetype among the canonical **Core 75** coding interview questions. Every problem features the precise problem statement, brute force analysis, core algorithmic breakthrough, optimal typed Python solution, edge-case unit assertions, runtime-generated execution trace, Big-O complexity breakdown, and follow-up interviewer variants.

---

## Master Core 75 Architecture & Category Blueprint

| # | Problem Name | Category | Difficulty | Primary Pattern | Time | Space |
| :-: | :--- | :--- | :---: | :--- | :---: | :---: |
| 1 | [Two Sum](#problem-1-p01-two-sum) | Arrays & Hashing | Easy | Arrays & Hashing | $O(N)$ | $O(N)$ |
| 2 | [Contains Duplicate](#problem-2-p02-contains-duplicate) | Arrays & Hashing | Easy | Arrays & Hashing | $O(N)$ | $O(N)$ |
| 3 | [Valid Anagram](#problem-3-p03-valid-anagram) | Arrays & Hashing | Easy | Arrays & Hashing | $O(N)$ | $O(1)$ |
| 4 | [Group Anagrams](#problem-4-p04-group-anagrams) | Arrays & Hashing | Medium | Arrays & Hashing | $O(N | $O(N |
| 5 | [Top K Frequent Elements](#problem-5-p05-top-k-frequent) | Arrays & Hashing | Medium | Arrays & Hashing | $O(N)$ | $O(N)$ |
| 6 | [Product of Array Except Self](#problem-6-p06-product-except-self) | Arrays & Hashing | Medium | Arrays & Hashing | $O(N)$ | $O(1)$ |
| 7 | [Encode and Decode Strings](#problem-7-p07-encode-and-decode-strings) | Arrays & Hashing | Medium | Arrays & Hashing | $O(N)$ | $O(1)$ |
| 8 | [Longest Consecutive Sequence](#problem-8-p08-longest-consecutive-sequence) | Arrays & Hashing | Medium | Arrays & Hashing | $O(N)$ | $O(N)$ |
| 9 | [Valid Palindrome](#problem-9-p09-valid-palindrome) | Two Pointers | Easy | Two Pointers | $O(N)$ | $O(1)$ |
| 10 | [3Sum](#problem-10-p10-three-sum) | Two Pointers | Medium | Two Pointers | $O(N^2)$ | $O(1)$ |
| 11 | [Container With Most Water](#problem-11-p11-container-with-most-water) | Two Pointers | Medium | Two Pointers | $O(N)$ | $O(1)$ |
| 12 | [Trapping Rain Water](#problem-12-p12-trapping-rain-water) | Two Pointers | Hard | Two Pointers | $O(N)$ | $O(1)$ |
| 13 | [Best Time to Buy and Sell Stock](#problem-13-p13-best-time-to-buy-and-sell-stock) | Sliding Window | Easy | Sliding Window | $O(N)$ | $O(1)$ |
| 14 | [Longest Substring Without Repeating Characters](#problem-14-p14-longest-substring-without-repeating-characters) | Sliding Window | Medium | Sliding Window | $O(N)$ | $O(\min(N, |
| 15 | [Longest Repeating Character Replacement](#problem-15-p15-longest-repeating-character-replacement) | Sliding Window | Medium | Sliding Window | $O(N)$ | $O(1)$ |
| 16 | [Minimum Window Substring](#problem-16-p16-minimum-window-substring) | Sliding Window | Hard | Sliding Window | $O(M | $O(M |
| 17 | [Valid Parentheses](#problem-17-p17-valid-parentheses) | Stack | Easy | Stack | $O(N)$ | $O(N)$ |
| 18 | [Daily Temperatures](#problem-18-p18-daily-temperatures) | Stack | Medium | Stack | $O(N)$ | $O(N)$ |
| 19 | [Largest Rectangle in Histogram](#problem-19-p19-largest-rectangle-in-histogram) | Stack | Hard | Stack | $O(N)$ | $O(N)$ |
| 20 | [Binary Search](#problem-20-p20-binary-search) | Binary Search | Easy | Binary Search | $O(\log | $O(1)$ |
| 21 | [Search in Rotated Sorted Array](#problem-21-p21-search-in-rotated-sorted-array) | Binary Search | Medium | Binary Search | $O(\log | $O(1)$ |
| 22 | [Find Minimum in Rotated Sorted Array](#problem-22-p22-find-minimum-in-rotated-sorted-array) | Binary Search | Medium | Binary Search | $O(\log | $O(1)$ |
| 23 | [Reverse Linked List](#problem-23-p23-reverse-linked-list) | Linked List | Easy | Linked List | $O(N)$ | $O(1)$ |
| 24 | [Merge Two Sorted Lists](#problem-24-p24-merge-two-sorted-lists) | Linked List | Easy | Linked List | $O(N | $O(1)$ |
| 25 | [Reorder List](#problem-25-p25-reorder-list) | Linked List | Medium | Linked List | $O(N)$ | $O(1)$ |
| 26 | [Remove Nth Node From End of List](#problem-26-p26-remove-nth-from-end) | Linked List | Medium | Linked List | $O(N)$ | $O(1)$ |
| 27 | [Linked List Cycle](#problem-27-p27-linked-list-cycle) | Linked List | Easy | Linked List | $O(N)$ | $O(1)$ |
| 28 | [Merge K Sorted Lists](#problem-28-p28-merge-k-sorted-lists) | Linked List | Hard | Linked List | $O(N | $O(k)$ |
| 29 | [Invert Binary Tree](#problem-29-p29-invert-binary-tree) | Trees | Easy | Trees | $O(N)$ | $O(H)$ |
| 30 | [Maximum Depth of Binary Tree](#problem-30-p30-maximum-depth-of-binary-tree) | Trees | Easy | Trees | $O(N)$ | $O(H)$ |
| 31 | [Same Tree](#problem-31-p31-same-tree) | Trees | Easy | Trees | $O(N)$ | $O(H)$ |
| 32 | [Subtree of Another Tree](#problem-32-p32-subtree-of-another-tree) | Trees | Easy | Trees | $O(N | $O(H)$ |
| 33 | [Lowest Common Ancestor of a BST](#problem-33-p33-lowest-common-ancestor-of-a-bst) | Trees | Medium | Trees | $O(H)$ | $O(1)$ |
| 34 | [Binary Tree Level Order Traversal](#problem-34-p34-binary-tree-level-order-traversal) | Trees | Medium | Trees | $O(N)$ | $O(N)$ |
| 35 | [Validate Binary Search Tree](#problem-35-p35-validate-binary-search-tree) | Trees | Medium | Trees | $O(N)$ | $O(H)$ |
| 36 | [Kth Smallest Element in a BST](#problem-36-p36-kth-smallest-element-in-a-bst) | Trees | Medium | Trees | $O(H | $O(H)$ |
| 37 | [Construct Binary Tree from Preorder and Inorder Traversal](#problem-37-p37-construct-binary-tree-from-preorder-and-inorder-traversal) | Trees | Medium | Trees | $O(N)$ | $O(N)$ |
| 38 | [Binary Tree Maximum Path Sum](#problem-38-p38-binary-tree-maximum-path-sum) | Trees | Hard | Trees | $O(N)$ | $O(H)$ |
| 39 | [Implement Trie (Prefix Tree)](#problem-39-p39-implement-trie) | Tries | Medium | Tries | $O(L)$ | $O(N |
| 40 | [Design Add and Search Words Data Structure](#problem-40-p40-design-add-and-search-words-data-structure) | Tries | Medium | Tries | $O(L)$ | $O(N |
| 41 | [Word Search II](#problem-41-p41-word-search-ii) | Tries | Hard | Tries | $O(M | $O(\sum |
| 42 | [Kth Largest Element in an Array](#problem-42-p42-kth-largest-element-in-an-array) | Heap / Priority Queue | Medium | Heap / Priority Queue | $O(N | $O(k)$ |
| 43 | [Find Median from Data Stream](#problem-43-p43-find-median-from-data-stream) | Heap / Priority Queue | Hard | Heap / Priority Queue | $O(\log | $O(N)$ |
| 44 | [Combination Sum](#problem-44-p44-combination-sum) | Backtracking | Medium | Backtracking | $O(N^{\frac{T}{M}})$ | $O(\frac{T}{M})$ |
| 45 | [Word Search](#problem-45-p45-word-search) | Backtracking | Medium | Backtracking | $O(M | $O(L)$ |
| 46 | [Subsets](#problem-46-p46-subsets) | Backtracking | Medium | Backtracking | $O(N | $O(N)$ |
| 47 | [Number of Islands](#problem-47-p47-number-of-islands) | Graphs | Medium | Graphs | $O(M | $O(M |
| 48 | [Clone Graph](#problem-48-p48-clone-graph) | Graphs | Medium | Graphs | $O(V | $O(V)$ |
| 49 | [Pacific Atlantic Water Flow](#problem-49-p49-pacific-atlantic-water-flow) | Graphs | Medium | Graphs | $O(M | $O(M |
| 50 | [Course Schedule](#problem-50-p50-course-schedule) | Graphs | Medium | Graphs | $O(V | $O(V |
| 51 | [Number of Connected Components in an Undirected Graph](#problem-51-p51-number-of-connected-components) | Graphs | Medium | Graphs | $O(V | $O(V)$ |
| 52 | [Graph Valid Tree](#problem-52-p52-graph-valid-tree) | Graphs | Medium | Graphs | $O(V | $O(V)$ |
| 53 | [Network Delay Time](#problem-53-p53-network-delay-time) | Graphs | Medium | Graphs | $O(E | $O(V |
| 54 | [Alien Dictionary](#problem-54-p54-alien-dictionary) | Graphs | Hard | Graphs | $O(C)$ | $O(U |
| 55 | [Climbing Stairs](#problem-55-p55-climbing-stairs) | Dynamic Programming | Easy | Dynamic Programming | $O(N)$ | $O(1)$ |
| 56 | [House Robber](#problem-56-p56-house-robber) | Dynamic Programming | Medium | Dynamic Programming | $O(N)$ | $O(1)$ |
| 57 | [House Robber II](#problem-57-p57-house-robber-ii) | Dynamic Programming | Medium | Dynamic Programming | $O(N)$ | $O(1)$ |
| 58 | [Coin Change](#problem-58-p58-coin-change) | Dynamic Programming | Medium | Dynamic Programming | $O(A | $O(A)$ |
| 59 | [Longest Increasing Subsequence](#problem-59-p59-longest-increasing-subsequence) | Dynamic Programming | Medium | Dynamic Programming | $O(N | $O(N)$ |
| 60 | [Word Break](#problem-60-p60-word-break) | Dynamic Programming | Medium | Dynamic Programming | $O(N | $O(N)$ |
| 61 | [Combination Sum IV](#problem-61-p61-combination-sum-iv) | Dynamic Programming | Medium | Dynamic Programming | $O(T | $O(T)$ |
| 62 | [Decode Ways](#problem-62-p62-decode-ways) | Dynamic Programming | Medium | Dynamic Programming | $O(N)$ | $O(N)$ |
| 63 | [Unique Paths](#problem-63-p63-unique-paths) | Dynamic Programming | Medium | Dynamic Programming | $O(m | $O(n)$ |
| 64 | [Longest Common Subsequence](#problem-64-p64-longest-common-subsequence) | Dynamic Programming | Medium | Dynamic Programming | $O(M | $O(M |
| 65 | [Edit Distance](#problem-65-p65-edit-distance) | Dynamic Programming | Medium | Dynamic Programming | $O(M | $O(M |
| 66 | [Partition Equal Subset Sum](#problem-66-p66-partition-equal-subset-sum) | Dynamic Programming | Medium | Dynamic Programming | $O(N | $O(\text{target})$ |
| 67 | [Jump Game](#problem-67-p67-jump-game) | Dynamic Programming | Medium | Dynamic Programming | $O(N)$ | $O(1)$ |
| 68 | [Insert Interval](#problem-68-p68-insert-interval) | Intervals | Medium | Intervals | $O(N)$ | $O(N)$ |
| 69 | [Merge Intervals](#problem-69-p69-merge-intervals) | Intervals | Medium | Intervals | $O(N | $O(N)$ |
| 70 | [Non-overlapping Intervals](#problem-70-p70-non-overlapping-intervals) | Intervals | Medium | Intervals | $O(N | $O(1)$ |
| 71 | [Meeting Rooms](#problem-71-p71-meeting-rooms) | Intervals | Easy | Intervals | $O(N | $O(1)$ |
| 72 | [Meeting Rooms II](#problem-72-p72-meeting-rooms-ii) | Intervals | Medium | Intervals | $O(N | $O(N)$ |
| 73 | [Number of 1 Bits](#problem-73-p73-number-of-1-bits) | Bit Manipulation | Easy | Bit Manipulation | $O(K)$ | $O(1)$ |
| 74 | [Counting Bits](#problem-74-p74-counting-bits) | Bit Manipulation | Easy | Bit Manipulation | $O(N)$ | $O(1)$ |
| 75 | [Missing Number](#problem-75-p75-missing-number) | Bit Manipulation | Easy | Bit Manipulation | $O(N)$ | $O(1)$ |

---

## Problem 1: Two Sum (Easy - Arrays & Hashing)

### Problem Statement
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. Each input has exactly one solution, and you may not use the same element twice.

### Brute Force Approach & Complexity
Iterate through all pairs $(i, j)$ with nested loops and check if `nums[i] + nums[j] == target`. Time: $O(N^2)$, Space: $O(1)$.

### Key Insight ("Aha!" Moment)
As we scan each number $x$, the required complement is $target - x$. Store visited numbers and their indices in a hash map for $O(1)$ lookup time.

### Optimal Python Solution
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """Finds indices of two numbers that add up to target.
    
    Time: O(N), Space: O(N)
    """
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### Edge-Case Asserts
```python
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]
```

### Dry-Run Execution Trace
```text
Input: nums = [2, 7, 11, 15], target = 9
Step  | i   | num   | complement   | seen map             | Action         
--------------------------------------------------------------------
1     | 0   | 2     | 7            | {}                   | Insert 2 -> 0
2     | 1   | 7     | 2            | {2: 0}               | Found! [0, 1]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single-pass linear scan across $N$ elements.
- **Space Complexity:** $O(N)$ to store up to $N$ elements in the hash map.

### Follow-Up Interview Variants
What if the input array is already sorted? Use Two Pointers (left = 0, right = N - 1) for $O(N)$ time and $O(1)$ auxiliary space.

---

## Problem 2: Contains Duplicate (Easy - Arrays & Hashing)

### Problem Statement
Given an integer array `nums`, return `True` if any value appears at least twice in the array, and return `False` if every element is distinct.

### Brute Force Approach & Complexity
Compare every pair with nested loops ($O(N^2)$ time, $O(1)$ space) or sort the array and check adjacent elements ($O(N \log N)$ time, $O(1)$ space).

### Key Insight ("Aha!" Moment)
Insert elements into a hash set. If an element is already in the set, a duplicate is found immediately in $O(1)$ average time.

### Optimal Python Solution
```python
def contains_duplicate(nums: list[int]) -> bool:
    """Checks if any element appears at least twice.
    
    Time: O(N), Space: O(N)
    """
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

### Edge-Case Asserts
```python
assert contains_duplicate([1, 2, 3, 1]) is True
assert contains_duplicate([1, 2, 3, 4]) is False
assert contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
assert contains_duplicate([]) is False
```

### Dry-Run Execution Trace
```text
Input: nums = [1, 2, 3, 1]
Step  | num   | seen set           | Status         
------------------------------------------------
1     | 1     | []                 | Added to set
2     | 2     | [1]                | Added to set
3     | 3     | [1, 2]             | Added to set
4     | 1     | [1, 2, 3]          | Duplicate detected! True
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ average time to scan array and insert into set.
- **Space Complexity:** $O(N)$ memory to store unique elements in the set.

### Follow-Up Interview Variants
What if space must be $O(1)$ and modifying input is allowed? Sort in-place in $O(N \log N)$ time and check adjacent items.

---

## Problem 3: Valid Anagram (Easy - Arrays & Hashing)

### Problem Statement
Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.

### Brute Force Approach & Complexity
Sort both strings and compare character-by-character. Time: $O(N \log N)$, Space: $O(N)$ or $O(1)$ depending on sort implementation.

### Key Insight ("Aha!" Moment)
An anagram has identical character frequency distributions. Compare frequency counters using an array of size 26 or a hash map.

### Optimal Python Solution
```python
def is_anagram(s: str, t: str) -> bool:
    """Checks if t is an anagram of s.
    
    Time: O(N), Space: O(1) assuming fixed 26-char alphabet.
    """
    if len(s) != len(t):
        return False
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in t:
        if ch not in counts or counts[ch] == 0:
            return False
        counts[ch] -= 1
    return True
```

### Edge-Case Asserts
```python
assert is_anagram("anagram", "nagaram") is True
assert is_anagram("rat", "car") is False
assert is_anagram("a", "ab") is False
assert is_anagram("", "") is True
```

### Dry-Run Execution Trace
```text
Input: s = 'anagram', t = 'nagaram'
Initial counts from s: {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}
Char   | Counts state after decrement        | Valid?    
-------------------------------------------------------
n      | {'a': 3, 'n': 0, 'g': 1, 'r': 1, 'm': 1} | True
a      | {'a': 2, 'n': 0, 'g': 1, 'r': 1, 'm': 1} | True
g      | {'a': 2, 'n': 0, 'g': 0, 'r': 1, 'm': 1} | True
a      | {'a': 1, 'n': 0, 'g': 0, 'r': 1, 'm': 1} | True
r      | {'a': 1, 'n': 0, 'g': 0, 'r': 0, 'm': 1} | True
a      | {'a': 0, 'n': 0, 'g': 0, 'r': 0, 'm': 1} | True
m      | {'a': 0, 'n': 0, 'g': 0, 'r': 0, 'm': 0} | True
All counts zero: True
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ where $N = \text{len}(s)$. Single pass over both strings.
- **Space Complexity:** $O(1)$ auxiliary space since alphabet size is bounded by 26 ASCII characters ($O(k)$ for general Unicode).

### Follow-Up Interview Variants
What if the inputs contain Unicode characters? Use a general hash map `dict[str, int]` instead of a fixed 26-element array.

---

## Problem 4: Group Anagrams (Medium - Arrays & Hashing)

### Problem Statement
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

### Brute Force Approach & Complexity
For each pair of strings, check if they are anagrams. Time: $O(N^2 \cdot K)$, Space: $O(N \cdot K)$.

### Key Insight ("Aha!" Moment)
Anagrams share the exact same character frequency counts. Use a 26-character count tuple (or sorted string) as the hash map key to bucket words.

### Optimal Python Solution
```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Groups strings that are anagrams of each other.
    
    Time: O(N * K), Space: O(N * K)
    """
    groups: dict[tuple[int, ...], list[str]] = {}
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        key = tuple(count)
        groups.setdefault(key, []).append(s)
    return list(groups.values())
```

### Edge-Case Asserts
```python
res1 = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
assert sorted([sorted(g) for g in res1]) == sorted([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
assert group_anagrams([""]) == [[""]]
assert group_anagrams(["a"]) == [["a"]]
```

### Dry-Run Execution Trace
```text
Input: ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
Word   | Key (Sorted/Tuple)   | Groups Count
------------------------------------------
eat    | aet                  | 1           
tea    | aet                  | 1           
tan    | ant                  | 2           
ate    | aet                  | 2           
nat    | ant                  | 2           
bat    | abt                  | 3           
Result: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

### Complexity Analysis
- **Time Complexity:** $O(N \cdot K)$ where $N$ is number of strings and $K$ is maximum string length.
- **Space Complexity:** $O(N \cdot K)$ to store strings grouped in the hash table.

### Follow-Up Interview Variants
What if character set is arbitrary UTF-8 strings? Sort each word in $O(K \log K)$ to form the key, yielding $O(N K \log K)$ time.

---

## Problem 5: Top K Frequent Elements (Medium - Arrays & Hashing)

### Problem Statement
Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

### Brute Force Approach & Complexity
Count frequencies with a hash map, then sort all unique items by frequency in descending order. Time: $O(N \log N)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Use Bucket Sort where index represents frequency (from $0$ to $N$). Since maximum frequency is $N$, filling and reverse-scanning buckets takes strictly $O(N)$ linear time.

### Optimal Python Solution
```python
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Returns the k most frequent elements using bucket sort.
    
    Time: O(N), Space: O(N)
    """
    counts: dict[int, int] = {}
    for num in nums:
        counts[num] = counts.get(num, 0) + 1
    
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for val, freq in counts.items():
        buckets[freq].append(val)
    
    res: list[int] = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            res.append(num)
            if len(res) == k:
                return res
    return res
```

### Edge-Case Asserts
```python
assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
assert top_k_frequent([1], 1) == [1]
assert sorted(top_k_frequent([4, 1, -1, 2, -1, 2, 3], 2)) == [-1, 2]
```

### Dry-Run Execution Trace
```text
Input: nums = [1, 1, 1, 2, 2, 3], k = 2
Frequencies: {1: 3, 2: 2, 3: 1}
Buckets (index = frequency):
  Freq 3: [1]
  Freq 2: [2]
  Freq 1: [3]
Extracting top 2 elements from highest frequency downwards: [1, 2]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ time using frequency bucket sorting.
- **Space Complexity:** $O(N)$ space for count hash map and frequency buckets.

### Follow-Up Interview Variants
What if $k \ll N$ and data is streaming? Maintain a min-heap of size $k$ in $O(N \log k)$ time and $O(k)$ memory.

---

## Problem 6: Product of Array Except Self (Medium - Arrays & Hashing)

### Problem Statement
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`. Must run in $O(N)$ time without using division.

### Brute Force Approach & Complexity
For each index $i$, iterate through all other indices $j \ne i$ and multiply their values. Time: $O(N^2)$, Space: $O(1)$.

### Key Insight ("Aha!" Moment)
Any element's product except self equals $(\text{prefix product to left of } i) \times (\text{suffix product to right of } i)$. Build the result in-place using two sequential passes.

### Optimal Python Solution
```python
def product_except_self(nums: list[int]) -> list[int]:
    """Computes product of array except self without division.
    
    Time: O(N), Space: O(1) auxiliary (output array excluded)
    """
    n = len(nums)
    res = [1] * n
    
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
        
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
        
    return res
```

### Edge-Case Asserts
```python
assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
assert product_except_self([2, 3]) == [3, 2]
```

### Dry-Run Execution Trace
```text
Input: [1, 2, 3, 4]
--- Prefix Pass (left-to-right) ---
i = 0 | res[0] = prefix (1) | prefix *= nums[0] -> 1
i = 1 | res[1] = prefix (1) | prefix *= nums[1] -> 2
i = 2 | res[2] = prefix (2) | prefix *= nums[2] -> 6
i = 3 | res[3] = prefix (6) | prefix *= nums[3] -> 24
res after prefix: [1, 1, 2, 6]
--- Suffix Pass (right-to-left) ---
i = 3 | res[3] = res[3] * suffix (6 * 1 = 6)
i = 2 | res[2] = res[2] * suffix (2 * 4 = 8)
i = 1 | res[1] = res[1] * suffix (1 * 12 = 12)
i = 0 | res[0] = res[0] * suffix (1 * 24 = 24)
Final output: [24, 12, 8, 6]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ with two linear passes.
- **Space Complexity:** $O(1)$ auxiliary memory (output array does not count toward space complexity).

### Follow-Up Interview Variants
How to handle multiple zeros in the array? The prefix/suffix logic naturally handles zero, one, or multiple zeros without divide-by-zero errors.

---

## Problem 7: Encode and Decode Strings (Medium - Arrays & Hashing)

### Problem Statement
Design an algorithm to encode a list of strings to a single string, and decode that string back to the original list of strings. The strings can contain any possible characters, including delimiters like '#' and commas.

### Brute Force Approach & Complexity
Using a fixed delimiter like comma or semicolon breaks immediately if strings contain that delimiter.

### Key Insight ("Aha!" Moment)
Prefix each string with its length and a delimiter: `<length>#<string>`. When decoding, reading `<length>` tells exactly how many subsequent bytes belong to the word regardless of characters inside it.

### Optimal Python Solution
```python
class Codec:
    def encode(self, strs: list[str]) -> str:
        """Encodes a list of strings to a single string."""
        res = []
        for s in strs:
            res.append(f"{len(s)}#{s}")
        return "".join(res)

    def decode(self, s: str) -> list[str]:
        """Decodes a single string to a list of strings."""
        res = []
        i = 0
        while i < len(s):
            j = s.find("#", i)
            length = int(s[i:j])
            word = s[j + 1 : j + 1 + length]
            res.append(word)
            i = j + 1 + length
        return res
```

### Edge-Case Asserts
```python
c = Codec()
assert c.decode(c.encode(["lint", "code", "love", "you"])) == ["lint", "code", "love", "you"]
assert c.decode(c.encode(["#", "##", "3#cat"])) == ["#", "##", "3#cat"]
assert c.decode(c.encode(["", ""])) == ["", ""]
assert c.decode(c.encode([])) == []
```

### Dry-Run Execution Trace
```text
Input strings: ['lint', 'code', 'love', 'you']
Encoded string: '4#lint4#code4#love3#you'
Step  | Delimiter Pos   | Length   | Extracted Word 
------------------------------------------------
1     | 1               | 4        | 'lint'
2     | 7               | 4        | 'code'
3     | 13              | 4        | 'love'
4     | 19              | 3        | 'you'
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ total characters processed during encode and decode.
- **Space Complexity:** $O(1)$ auxiliary space beyond storing the output strings.

### Follow-Up Interview Variants
How does this protocol compare to HTTP chunked transfer encoding? It uses the exact same framing principle (hex length + CRLF + payload).

---

## Problem 8: Longest Consecutive Sequence (Medium - Arrays & Hashing)

### Problem Statement
Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. Must run in $O(N)$ time.

### Brute Force Approach & Complexity
Sort the array and count longest adjacent run. Time: $O(N \log N)$, Space: $O(1)$ or $O(N)$.

### Key Insight ("Aha!" Moment)
Insert all numbers into a hash set. Only begin counting a streak if `num - 1` is NOT in the set (i.e. `num` is the start of a streak). Each number is visited at most twice.

### Optimal Python Solution
```python
def longest_consecutive(nums: list[int]) -> int:
    """Finds length of longest consecutive sequence in O(N) time."""
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Check if num is the start of a sequence
        if (num - 1) not in num_set:
            current_num = num
            current_streak = 1
            while (current_num + 1) in num_set:
                current_num += 1
                current_streak += 1
            longest = max(longest, current_streak)
            
    return longest
```

### Edge-Case Asserts
```python
assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert longest_consecutive([]) == 0
assert longest_consecutive([1, 2, 0, 1]) == 3
```

### Dry-Run Execution Trace
```text
Input: [100, 4, 200, 1, 3, 2]
Set: {1, 2, 3, 100, 4, 200}
Num   | Is Sequence Start? (x-1 not in set) | Streak Length  
------------------------------------------------------------
100   | True                                | 1 (explored [100])
4     | False                               | Skipped
200   | True                                | 1 (explored [200])
1     | True                                | 4 (explored [1, 2, 3, 4])
3     | False                               | Skipped
2     | False                               | Skipped
Max streak: 4
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ time because each number is only checked as a sequence start once.
- **Space Complexity:** $O(N)$ memory to store unique numbers in the hash set.

### Follow-Up Interview Variants
Could you use Union-Find (Disjoint Set Union) instead? Yes, union `num` with `num + 1` if present, maintaining component sizes in $O(N \alpha(N))$ time.

---

## Problem 9: Valid Palindrome (Easy - Two Pointers)

### Problem Statement
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

### Brute Force Approach & Complexity
Filter the string into a new cleaned string and reverse it. Time: $O(N)$, Space: $O(N)$ extra memory.

### Key Insight ("Aha!" Moment)
Use two pointers starting at left and right extremes. Advance inward skipping non-alphanumeric characters, comparing lowercased characters in-place with $O(1)$ space.

### Optimal Python Solution
```python
def is_palindrome(s: str) -> bool:
    """Checks if string is palindrome ignoring non-alphanumeric chars.
    
    Time: O(N), Space: O(1)
    """
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

### Edge-Case Asserts
```python
assert is_palindrome("A man, a plan, a canal: Panama") is True
assert is_palindrome("race a car") is False
assert is_palindrome(" ") is True
assert is_palindrome("0P") is False
```

### Dry-Run Execution Trace
```text
Input: 'A man, a plan, a canal: Panama'
left  | ch[left]   | right | ch[right]  | Match?    
------------------------------------------------
0     | 'A' (a) | 29    | 'a' (a) | True
2     | 'm' (m) | 28    | 'm' (m) | True
3     | 'a' (a) | 27    | 'a' (a) | True
4     | 'n' (n) | 26    | 'n' (n) | True
7     | 'a' (a) | 25    | 'a' (a) | True
9     | 'p' (p) | 24    | 'P' (p) | True
10    | 'l' (l) | 21    | 'l' (l) | True
11    | 'a' (a) | 20    | 'a' (a) | True
12    | 'n' (n) | 19    | 'n' (n) | True
15    | 'a' (a) | 18    | 'a' (a) | True
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single pass across length $N$.
- **Space Complexity:** $O(1)$ auxiliary space without allocating a cleaned string.

### Follow-Up Interview Variants
What if you are allowed to remove at most one character to form a valid palindrome? Recursively check the two branches (`left + 1` or `right - 1`) on first mismatch.

---

## Problem 10: 3Sum (Medium - Two Pointers)

### Problem Statement
Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.

### Brute Force Approach & Complexity
Generate all triplets with 3 nested loops and store them in a set to avoid duplicates. Time: $O(N^3)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Sort the array in $O(N \log N)$. Fix element $i$, then use two pointers (`left = i + 1`, `right = N - 1`) to find pairs adding to `-nums[i]`. Skip duplicate adjacent elements to avoid duplicate triplets.

### Optimal Python Solution
```python
def three_sum(nums: list[int]) -> list[list[int]]:
    """Finds all unique triplets that sum to zero.
    
    Time: O(N^2), Space: O(1) auxiliary
    """
    nums.sort()
    res: list[list[int]] = []
    
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                res.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
                
    return res
```

### Edge-Case Asserts
```python
assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
assert three_sum([0, 1, 1]) == []
assert three_sum([0, 0, 0]) == [[0, 0, 0]]
```

### Dry-Run Execution Trace
```text
Sorted input: [-4, -1, -1, 0, 1, 2]
i   | nums[i]  | left  | right | Sum    | Action                   
-------------------------------------------------------
0   | -4       | 1     | 5     | -3     | sum < 0 -> left++
0   | -4       | 2     | 5     | -3     | sum < 0 -> left++
0   | -4       | 3     | 5     | -2     | sum < 0 -> left++
0   | -4       | 4     | 5     | -1     | sum < 0 -> left++
1   | -1       | 2     | 5     | 0      | Found! [-1,-1,2]
1   | -1       | 3     | 4     | 0      | Found! [-1,0,1]
3   | 0        | 4     | 5     | 3      | sum > 0 -> right--
```

### Complexity Analysis
- **Time Complexity:** $O(N^2)$ time ($O(N \log N)$ sort + $N$ iterations of two-pointer scans).
- **Space Complexity:** $O(1)$ auxiliary space (or $O(N)$ depending on sorting algorithm implementation).

### Follow-Up Interview Variants
How to extend to 4Sum or KSum? Recursively reduce KSum to $(K-1)\text{Sum}$ until reaching 2Sum base case with two pointers in $O(N^{K-1})$.

---

## Problem 11: Container With Most Water (Medium - Two Pointers)

### Problem Statement
You are given an integer array `height` of length $n$. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.

### Brute Force Approach & Complexity
Compute area for all pairs $(i, j)$ where $\text{area} = (j - i) \times \min(h[i], h[j])$. Time: $O(N^2)$, Space: $O(1)$.

### Key Insight ("Aha!" Moment)
The width is initially maximized by placing pointers at $0$ and $N - 1$. The height is constrained by the shorter wall. Moving the taller wall can only decrease width without increasing height. Therefore, greedily advance the shorter wall inward.

### Optimal Python Solution
```python
def max_area(height: list[int]) -> int:
    """Finds maximum water container capacity using two pointers.
    
    Time: O(N), Space: O(1)
    """
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
            
    return max_water
```

### Edge-Case Asserts
```python
assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
assert max_area([1, 1]) == 1
assert max_area([4, 3, 2, 1, 4]) == 16
assert max_area([1, 2, 1]) == 2
```

### Dry-Run Execution Trace
```text
Input: [1, 8, 6, 2, 5, 4, 8, 3, 7]
Step  | left  | right | h[l]  | h[r]  | width  | area   | max_area  | Move      
-----------------------------------------------------------------
1     | 0     | 8     | 1     | 7     | 8      | 8      | 8         | left++    
2     | 1     | 8     | 8     | 7     | 7      | 49     | 49        | right--   
3     | 1     | 7     | 8     | 3     | 6      | 18     | 49        | right--   
4     | 1     | 6     | 8     | 8     | 5      | 40     | 49        | right--   
5     | 1     | 5     | 8     | 4     | 4      | 16     | 49        | right--   
6     | 1     | 4     | 8     | 5     | 3      | 15     | 49        | right--   
7     | 1     | 3     | 8     | 2     | 2      | 4      | 49        | right--   
8     | 1     | 2     | 8     | 6     | 1      | 6      | 49        | right--
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single pass as pointers move inward until they meet.
- **Space Complexity:** $O(1)$ constant memory.

### Follow-Up Interview Variants
What if you need to return the container indices instead of just area? Track the `(best_left, best_right)` pair whenever `max_water` updates.

---

## Problem 12: Trapping Rain Water (Hard - Two Pointers)

### Problem Statement
Given $n$ non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

### Brute Force Approach & Complexity
For each bar $i$, find the maximum to its left and maximum to its right with linear scans: $\text{water}[i] = \max(0, \min(L_{\max}, R_{\max}) - h[i])$. Time: $O(N^2)$, Space: $O(1)$.

### Key Insight ("Aha!" Moment)
Water trapped at index $i$ depends strictly on $\min(\text{max\_left}, \text{max\_right})$. With two pointers, whichever side has the smaller running maximum determines the water bound, allowing in-place computation with $O(1)$ space.

### Optimal Python Solution
```python
def trap_rain_water(height: list[int]) -> int:
    """Computes trapped rain water in O(N) time and O(1) space.
    
    Time: O(N), Space: O(1)
    """
    if not height:
        return 0

    left, right = 0, len(height) - 1
    max_left, max_right = 0, 0
    total_water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= max_left:
                max_left = height[left]
            else:
                total_water += max_left - height[left]
            left += 1
        else:
            if height[right] >= max_right:
                max_right = height[right]
            else:
                total_water += max_right - height[right]
            right -= 1

    return total_water
```

### Edge-Case Asserts
```python
assert trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
assert trap_rain_water([4, 2, 0, 3, 2, 5]) == 9
assert trap_rain_water([]) == 0
assert trap_rain_water([3, 3, 3]) == 0
```

### Dry-Run Execution Trace
```text
Input: height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
Step  | Branch  | left | right | h[l] | h[r] | max_l | max_r | Added | Total
----------------------------------------------------------------------
1     | Left    | 0    | 11    | 0    | 1    | 0     | 0     | 0     | 0    
2     | Right   | 1    | 11    | 1    | 1    | 0     | 1     | 0     | 0    
3     | Left    | 1    | 10    | 1    | 2    | 1     | 1     | 0     | 0    
4     | Left    | 2    | 10    | 0    | 2    | 1     | 1     | 1     | 1    
5     | Right   | 3    | 10    | 2    | 2    | 1     | 2     | 0     | 1    
6     | Right   | 3    | 9     | 2    | 1    | 1     | 2     | 1     | 2    
7     | Right   | 3    | 8     | 2    | 2    | 1     | 2     | 0     | 2    
8     | Left    | 3    | 7     | 2    | 3    | 2     | 2     | 0     | 2    
9     | Left    | 4    | 7     | 1    | 3    | 2     | 2     | 1     | 3    
10    | Left    | 5    | 7     | 0    | 3    | 2     | 2     | 2     | 5    
11    | Left    | 6    | 7     | 1    | 3    | 2     | 2     | 1     | 6    
Final Trapped Water: 6
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear time; every bar is processed exactly once.
- **Space Complexity:** $O(1)$ space using two pointers.

### Follow-Up Interview Variants
How to solve Trapping Rain Water in 2D (a 2D elevation grid)? Use a Min-Heap initialized with all boundary cells; pop the lowest boundary wall and traverse neighbors (Dijkstra's variant) in $O(R \cdot C \log(R \cdot C))$ time.

---

## Problem 13: Best Time to Buy and Sell Stock (Easy - Sliding Window)

### Problem Statement
You are given an array `prices` where `prices[i]` is the price of a given stock on the $i^{\text{th}}$ day. Maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

### Brute Force Approach & Complexity
Try every pair $(i, j)$ with $i < j$ and compute $\text{profit} = \text{prices}[j] - \text{prices}[i]$. Time: $O(N^2)$, Space: $O(1)$.

### Key Insight ("Aha!" Moment)
Maintain the running minimum purchase price seen so far. At each day $i$, the maximum profit attainable by selling on day $i$ is $\text{prices}[i] - \text{min\_price}$.

### Optimal Python Solution
```python
def max_profit(prices: list[int]) -> int:
    """Calculates maximum profit from a single buy and sell transaction.
    
    Time: O(N), Space: O(1)
    """
    min_price = float("inf")
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit
```

### Edge-Case Asserts
```python
assert max_profit([7, 1, 5, 3, 6, 4]) == 5
assert max_profit([7, 6, 4, 3, 1]) == 0
assert max_profit([1, 2]) == 1
assert max_profit([]) == 0
```

### Dry-Run Execution Trace
```text
Input: prices = [7, 1, 5, 3, 6, 4]
Day   | Price  | Min Price Seen   | Potential Profit   | Max Profit  
-----------------------------------------------------------------
1     | 7      | 7                | 0                  | 0           
2     | 1      | 1                | 0                  | 0           
3     | 5      | 1                | 4                  | 4           
4     | 3      | 1                | 2                  | 4           
5     | 6      | 1                | 5                  | 5           
6     | 4      | 1                | 3                  | 5
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single pass over array.
- **Space Complexity:** $O(1)$ constant auxiliary memory.

### Follow-Up Interview Variants
What if you can complete as many transactions as you like (Stock II)? Accumulate every positive adjacent price increment: $\sum \max(0, prices[i] - prices[i-1])$.

---

## Problem 14: Longest Substring Without Repeating Characters (Medium - Sliding Window)

### Problem Statement
Given a string `s`, find the length of the longest substring without duplicate characters.

### Brute Force Approach & Complexity
Generate all substrings $O(N^2)$ and check if each has unique characters $O(N)$. Time: $O(N^3)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Maintain a dynamic sliding window $[\text{left}, \text{right}]$ and a hash map of characters to their most recent index. When character $s[\text{right}]$ is seen inside the window, jump $\text{left}$ to $\text{last\_seen}[c] + 1$.

### Optimal Python Solution
```python
def length_of_longest_substring(s: str) -> int:
    """Finds length of longest substring without duplicate characters.
    
    Time: O(N), Space: O(min(N, M))
    """
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

### Edge-Case Asserts
```python
assert length_of_longest_substring("abcabcbb") == 3
assert length_of_longest_substring("bbbbb") == 1
assert length_of_longest_substring("pwwkew") == 3
assert length_of_longest_substring("") == 0
```

### Dry-Run Execution Trace
```text
Input: 'abcabcbb'
right | char  | left  | last_seen[char]    | Window Substring   | max_len 
--------------------------------------------------------------------
0     | 'a'   | 0     | None               | 'a'                | 1       
1     | 'b'   | 0     | None               | 'ab'               | 2       
2     | 'c'   | 0     | None               | 'abc'              | 3       
3     | 'a'   | 1     | 0                  | 'bca'              | 3       
4     | 'b'   | 2     | 1                  | 'cab'              | 3       
5     | 'c'   | 3     | 2                  | 'abc'              | 3       
6     | 'b'   | 5     | 4                  | 'cb'               | 3       
7     | 'b'   | 7     | 6                  | 'b'                | 3
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear time; both pointers advance strictly to the right.
- **Space Complexity:** $O(\min(N, M))$ where $M$ is alphabet size.

### Follow-Up Interview Variants
What if at most $K$ distinct characters are permitted? Use a frequency counter hash map; shrink window while $\text{len}(\text{counts}) > K$.

---

## Problem 15: Longest Repeating Character Replacement (Medium - Sliding Window)

### Problem Statement
You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character at most `k` times. Return the length of the longest substring containing the same letter you can get after performing above operations.

### Brute Force Approach & Complexity
Examine every substring, count frequencies, and verify if $(\text{length} - \text{max\_freq}) \le k$. Time: $O(N^2 \cdot 26)$, Space: $O(26)$.

### Key Insight ("Aha!" Moment)
A window $[\text{left}, \text{right}]$ is valid if $\text{window\_size} - \text{max\_frequency} \le k$. When this condition is violated, shrink the window from the left by one step.

### Optimal Python Solution
```python
def character_replacement(s: str, k: int) -> int:
    """Finds longest repeating character substring after at most k replacements.
    
    Time: O(N), Space: O(1)
    """
    counts: dict[str, int] = {}
    left = 0
    max_freq = 0
    max_len = 0
    
    for right in range(len(s)):
        ch = s[right]
        counts[ch] = counts.get(ch, 0) + 1
        max_freq = max(max_freq, counts[ch])
        
        while (right - left + 1) - max_freq > k:
            counts[s[left]] -= 1
            left += 1
            
        max_len = max(max_len, right - left + 1)
        
    return max_len
```

### Edge-Case Asserts
```python
assert character_replacement("ABAB", 2) == 4
assert character_replacement("AABABBA", 1) == 4
assert character_replacement("AAAA", 2) == 4
assert character_replacement("ABBB", 2) == 4
```

### Dry-Run Execution Trace
```text
Input: s = 'AABABBA', k = 1
right | char  | counts           | max_freq  | Window Len  | Valid?  | left 
-----------------------------------------------------------------
0     | 'A'   | {'A': 1}         | 1         | 1           | True    | 0    
1     | 'A'   | {'A': 2}         | 2         | 2           | True    | 0    
2     | 'B'   | {'A': 2, 'B': 1} | 2         | 3           | True    | 0    
3     | 'A'   | {'A': 3, 'B': 1} | 3         | 4           | True    | 0    
4     | 'B'   | {'A': 2, 'B': 2} | 3         | 5           | False   | 1    
5     | 'B'   | {'A': 1, 'B': 3} | 3         | 5           | False   | 2    
6     | 'A'   | {'A': 2, 'B': 2} | 3         | 5           | False   | 3
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ since both pointers only advance forward.
- **Space Complexity:** $O(1)$ auxiliary space bounded by 26 English uppercase characters.

### Follow-Up Interview Variants
Do we need to decrement `max_freq` when shrinking the window? No! A new maximum window length can only be achieved if `max_freq` strictly increases beyond its previous peak.

---

## Problem 16: Minimum Window Substring (Hard - Sliding Window)

### Problem Statement
Given two strings `s` and `t` of lengths $m$ and $n$ respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return empty string `""`.

### Brute Force Approach & Complexity
Examine every substring of $s$ ($O(N^2)$) and check if it contains all characters of $t$ in required frequencies ($O(N)$). Time: $O(N^3)$, Space: $O(M)$.

### Key Insight ("Aha!" Moment)
Maintain required counts `need` and current window counts `have`. Keep a count `matched` of how many distinct characters satisfy their requirement. Expand `right` until `matched == len(need)`, then greedily contract `left` while maintaining validity.

### Optimal Python Solution
```python
def min_window(s: str, t: str) -> str:
    """Finds minimum window substring of s containing all characters of t.
    
    Time: O(M + N), Space: O(M + N)
    """
    if not s or not t:
        return ""
        
    need: dict[str, int] = {}
    for c in t:
        need[c] = need.get(c, 0) + 1
        
    have: dict[str, int] = {}
    matched = 0
    left = 0
    min_len = float("inf")
    res_indices = (-1, -1)
    
    for right in range(len(s)):
        char = s[right]
        have[char] = have.get(char, 0) + 1
        
        if char in need and have[char] == need[char]:
            matched += 1
            
        while matched == len(need):
            if (right - left + 1) < min_len:
                min_len = right - left + 1
                res_indices = (left, right)
                
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                matched -= 1
            left += 1
            
    l, r = res_indices
    return s[l : r + 1] if min_len != float("inf") else ""
```

### Edge-Case Asserts
```python
assert min_window("ADOBECODEBANC", "ABC") == "BANC"
assert min_window("a", "a") == "a"
assert min_window("a", "aa") == ""
assert min_window("ab", "b") == "b"
```

### Dry-Run Execution Trace
```text
Input: s = 'ADOBECODEBANC', t = 'ABC'
Required characters: {'A': 1, 'B': 1, 'C': 1}
right | char  | matched  | left  | Window          | Action                   
----------------------------------------------------------------------
5     | 'C'   | 3        | 0     | 'ADOBEC' | Shrink left (best: 'ADOBEC')
10    | 'A'   | 3        | 1     | 'DOBECODEBA' | Shrink left (best: 'ADOBEC')
10    | 'A'   | 3        | 2     | 'OBECODEBA' | Shrink left (best: 'ADOBEC')
10    | 'A'   | 3        | 3     | 'BECODEBA' | Shrink left (best: 'ADOBEC')
10    | 'A'   | 3        | 4     | 'ECODEBA' | Shrink left (best: 'ADOBEC')
10    | 'A'   | 3        | 5     | 'CODEBA' | Shrink left (best: 'ADOBEC')
12    | 'C'   | 3        | 6     | 'ODEBANC' | Shrink left (best: 'ADOBEC')
12    | 'C'   | 3        | 7     | 'DEBANC' | Shrink left (best: 'ADOBEC')
12    | 'C'   | 3        | 8     | 'EBANC' | Shrink left (best: 'EBANC')
12    | 'C'   | 3        | 9     | 'BANC' | Shrink left (best: 'BANC')
Resulting minimum window: 'BANC'
```

### Complexity Analysis
- **Time Complexity:** $O(M + N)$ where $M = \text{len}(s)$ and $N = \text{len}(t)$. Each character is visited at most twice.
- **Space Complexity:** $O(M + N)$ to store character frequency maps.

### Follow-Up Interview Variants
What if $s$ contains billions of characters and can only be streamed? Keep only the filtered indices and characters that appear in $t$, reducing memory footprint to $O(N)$.

---

## Problem 17: Valid Parentheses (Easy - Stack)

### Problem Statement
Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

### Brute Force Approach & Complexity
Repeatedly replace occurrences of `"()"`, `"[]"`, and `"{}"` with `""` until no more replacements are possible. Time: $O(N^2)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
A LIFO stack matches the most recently opened bracket with the next closing bracket. Push opening brackets; on closing brackets, pop and check if it matches.

### Optimal Python Solution
```python
def is_valid_parentheses(s: str) -> bool:
    """Checks if bracket sequence is properly nested and closed.
    
    Time: O(N), Space: O(N)
    """
    stack: list[str] = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack
```

### Edge-Case Asserts
```python
assert is_valid_parentheses("()") is True
assert is_valid_parentheses("()[]{}") is True
assert is_valid_parentheses("(]") is False
assert is_valid_parentheses("([)]") is False
assert is_valid_parentheses("{[]}") is True
```

### Dry-Run Execution Trace
```text
Input: '()[]{}'
Step  | char  | Action          | Stack state    
---------------------------------------------
1     | '('   | Push open       | ['(']          
2     | ')'   | Pop match       | []             
3     | '['   | Push open       | ['[']          
4     | ']'   | Pop match       | []             
5     | '{'   | Push open       | ['{']          
6     | '}'   | Pop match       | []             
Is valid: True
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single pass across length $N$.
- **Space Complexity:** $O(N)$ to hold opening brackets on stack in worst case.

### Follow-Up Interview Variants
What if brackets include wildcards like `*` which can be `'('`, `')'`, or empty? Use two counters for minimum and maximum possible open bracket counts (Greedy Range Tracking).

---

## Problem 18: Daily Temperatures (Medium - Stack)

### Problem Statement
Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the $i^{\text{th}}$ day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0`.

### Brute Force Approach & Complexity
For each day $i$, scan ahead $j = i+1 \dots N$ until finding a higher temperature. Time: $O(N^2)$, Space: $O(1)$.

### Key Insight ("Aha!" Moment)
Maintain a **Monotonic Decreasing Stack** storing indices of unresolved cold days. When today's temperature is warmer than the top of the stack, pop and record the elapsed days.

### Optimal Python Solution
```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    """Calculates days until warmer temperature using monotonic stack.
    
    Time: O(N), Space: O(N)
    """
    n = len(temperatures)
    res = [0] * n
    stack: list[int] = []  # Stores indices
    
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev_i = stack.pop()
            res[prev_i] = i - prev_i
        stack.append(i)
        
    return res
```

### Edge-Case Asserts
```python
assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
assert daily_temperatures([30, 60, 90]) == [1, 1, 0]
assert daily_temperatures([]) == []
```

### Dry-Run Execution Trace
```text
Input: [73, 74, 75, 71, 69, 72, 76, 73]
i   | temp  | Stack [(idx, temp)]       | Popped idx & wait time   
-----------------------------------------------------------------
0   | 73    | [(0, 73)]                 | None                     
1   | 74    | [(1, 74)]                 | idx 0 waited 1d          
2   | 75    | [(2, 75)]                 | idx 1 waited 1d          
3   | 71    | [(2, 75), (3, 71)]        | None                     
4   | 69    | [(2, 75), (3, 71), (4, 69)] | None                     
5   | 72    | [(2, 75), (5, 72)]        | idx 4 waited 1d, idx 3 waited 2d
6   | 76    | [(6, 76)]                 | idx 5 waited 1d, idx 2 waited 4d
7   | 73    | [(6, 76), (7, 73)]        | None                     
Result: [1, 1, 4, 2, 1, 1, 0, 0]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear time; every index is pushed and popped at most once.
- **Space Complexity:** $O(N)$ auxiliary space for the stack.

### Follow-Up Interview Variants
Can this be solved in $O(1)$ extra space? Iterate backwards from the end of the array, using the already-computed answers to jump forward.

---

## Problem 19: Largest Rectangle in Histogram (Hard - Stack)

### Problem Statement
Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.

### Brute Force Approach & Complexity
For each pair of bars $(i, j)$, find the minimum height between them and multiply by $(j - i + 1)$. Time: $O(N^2)$, Space: $O(1)$.

### Key Insight ("Aha!" Moment)
Maintain a **Monotonic Increasing Stack** of `(index, height)`. When a shorter bar is encountered, pop previous bars because they cannot extend further right. The popped bar's width extends between the current index and the new stack top.

### Optimal Python Solution
```python
def largest_rectangle_area(heights: list[int]) -> int:
    """Computes maximum rectangle area using a monotonic increasing stack.
    
    Time: O(N), Space: O(N)
    """
    stack: list[tuple[int, int]] = []  # (index, height)
    max_area = 0
    
    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))
        
    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))
        
    return max_area
```

### Edge-Case Asserts
```python
assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
assert largest_rectangle_area([2, 4]) == 4
assert largest_rectangle_area([1]) == 1
assert largest_rectangle_area([]) == 0
```

### Dry-Run Execution Trace
```text
Input heights: [2, 1, 5, 6, 2, 3] (with appended sentinel 0: [2, 1, 5, 6, 2, 3, 0])
i   | h[i]  | Stack [(idx, h)]       | Popped & Evaluated Area       
-----------------------------------------------------------------
0   | 2     | [(0, 2)]               | None                          
1   | 1     | [(1, 1)]               | h=2*w=1->area=2               
2   | 5     | [(1, 1), (2, 5)]       | None                          
3   | 6     | [(1, 1), (2, 5), (3, 6)] | None                          
4   | 2     | [(1, 1), (4, 2)]       | h=6*w=1->area=6, h=5*w=2->area=10
5   | 3     | [(1, 1), (4, 2), (5, 3)] | None                          
6   | 0     | [(6, 0)]               | h=3*w=1->area=3, h=2*w=4->area=8, h=1*w=6->area=6
Maximum Rectangle Area: 10
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear time; each bar is pushed and popped at most once.
- **Space Complexity:** $O(N)$ stack memory.

### Follow-Up Interview Variants
How to solve Maximal Rectangle in a 2D binary matrix? Convert each row into a histogram of consecutive 1s and run this algorithm row-by-row in $O(R \cdot C)$.

---

## Problem 20: Binary Search (Easy - Binary Search)

### Problem Statement
Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.

### Brute Force Approach & Complexity
Linear scan through the array. Time: $O(N)$, Space: $O(1)$.

### Key Insight ("Aha!" Moment)
Because the array is sorted, comparing `target` with the midpoint `mid` eliminates half the remaining search space on every iteration.

### Optimal Python Solution
```python
def binary_search(nums: list[int], target: int) -> int:
    """Searches for target in sorted nums in O(log N) time."""
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1
```

### Edge-Case Asserts
```python
assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
assert binary_search([5], 5) == 0
assert binary_search([], 3) == -1
```

### Dry-Run Execution Trace
```text
Input: nums = [-1, 0, 3, 5, 9, 12], target = 9
Step  | left  | right | mid   | nums[mid]  | Action         
-------------------------------------------------------
1     | 0     | 5     | 2     | 3          | mid < target -> l = mid+1
2     | 3     | 5     | 4     | 9          | Target found at 4!
```

### Complexity Analysis
- **Time Complexity:** $O(\log N)$ logarithmic time.
- **Space Complexity:** $O(1)$ constant auxiliary space.

### Follow-Up Interview Variants
Why write `mid = left + (right - left) // 2` instead of `(left + right) // 2`? To avoid 32-bit integer overflow in languages like C++/Java when `left + right > 2^{31} - 1`.

---

## Problem 21: Search in Rotated Sorted Array (Medium - Binary Search)

### Problem Statement
There is an integer array `nums` sorted in ascending order (with distinct values), rotated at an unknown pivot index. Given `nums` and a `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

### Brute Force Approach & Complexity
Linear search $O(N)$ across all elements. Space: $O(1)$.

### Key Insight ("Aha!" Moment)
In any rotated sorted array, splitting at `mid` always leaves at least one half strictly sorted. Determine which half is sorted, check if `target` lies within that half's boundary, and bisect accordingly in $O(\log N)$.

### Optimal Python Solution
```python
def search_rotated(nums: list[int], target: int) -> int:
    """Searches for target in rotated sorted array in O(log N) time."""
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
            
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
                
    return -1
```

### Edge-Case Asserts
```python
assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
assert search_rotated([1], 0) == -1
assert search_rotated([1, 3], 3) == 1
```

### Dry-Run Execution Trace
```text
Input: nums = [4, 5, 6, 7, 0, 1, 2], target = 0
Step  | left  | right | mid   | nums[mid]  | Sorted Half     | Action         
----------------------------------------------------------------------
1     | 4     | 6     | 3     | 7          | Left [l..mid]   | l = mid + 1    
2     | 4     | 4     | 5     | 1          | Left [l..mid]   | r = mid - 1    
3     | 4     | 4     | 4     | 0          | -               | Found index 4!
```

### Complexity Analysis
- **Time Complexity:** $O(\log N)$ time logarithmic search.
- **Space Complexity:** $O(1)$ auxiliary memory.

### Follow-Up Interview Variants
What if duplicate elements are allowed? Worst case degrades to $O(N)$ when `nums[left] == nums[mid] == nums[right]` because neither half can be guaranteed sorted.

---

## Problem 22: Find Minimum in Rotated Sorted Array (Medium - Binary Search)

### Problem Statement
Suppose an array of length $n$ sorted in ascending order is rotated between 1 and $n$ times. Given the sorted rotated array `nums` of unique elements, return the minimum element of this array. Must run in $O(\log N)$ time.

### Brute Force Approach & Complexity
Linear scan to find the minimum element in $O(N)$ time. Space: $O(1)$.

### Key Insight ("Aha!" Moment)
Compare `nums[mid]` with `nums[right]`. If `nums[mid] > nums[right]`, the rotation pivot point (and minimum element) lies strictly to the right (`left = mid + 1`). Otherwise, the minimum is at `mid` or to the left (`right = mid`).

### Optimal Python Solution
```python
def find_min(nums: list[int]) -> int:
    """Finds minimum element in rotated sorted array in O(log N) time."""
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
            
    return nums[left]
```

### Edge-Case Asserts
```python
assert find_min([3, 4, 5, 1, 2]) == 1
assert find_min([4, 5, 6, 7, 0, 1, 2]) == 0
assert find_min([11, 13, 15, 17]) == 11
assert find_min([2, 1]) == 1
```

### Dry-Run Execution Trace
```text
Input: nums = [4, 5, 6, 7, 0, 1, 2]
Step  | left  | right | mid   | nums[mid]  | nums[right]  | Action         
-----------------------------------------------------------------
1     | 0     | 6     | 3     | 7          | 2            | l = mid + 1 (inflection right)
2     | 4     | 6     | 5     | 1          | 2            | r = mid (inflection at or left)
3     | 4     | 5     | 4     | 0          | 1            | r = mid (inflection at or left)
Minimum element at index 4 is 0
```

### Complexity Analysis
- **Time Complexity:** $O(\log N)$ binary search time.
- **Space Complexity:** $O(1)$ constant space.

### Follow-Up Interview Variants
How many times was the array rotated? The index of the minimum element equals the number of clockwise rotation shifts.

---

## Problem 23: Reverse Linked List (Easy - Linked List)

### Problem Statement
Given the `head` of a singly linked list, reverse the list, and return the reversed list.

### Brute Force Approach & Complexity
Store all node values into an array, reverse the array, and reconstruct the linked list. Time: $O(N)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Iterate through the list with three pointers: `prev`, `curr`, and `next_node`. Invert each pointer (`curr.next = prev`) in-place in $O(1)$ space.

### Optimal Python Solution
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverses singly linked list in-place in O(N) time, O(1) space."""
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

### Edge-Case Asserts
```python
# Helper to build and read
def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

assert to_list(reverse_list(from_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
assert to_list(reverse_list(from_list([1, 2]))) == [2, 1]
assert to_list(reverse_list(from_list([]))) == []
```

### Dry-Run Execution Trace
```text
Input linked list: 1 -> 2 -> 3 -> 4 -> 5 -> None
Step  | curr   | prev   | next_node  | Action                   
-------------------------------------------------------
1     | 1      | None   | 2          | curr.next = prev, prev = curr
2     | 2      | 1      | 3          | curr.next = prev, prev = curr
3     | 3      | 2      | 4          | curr.next = prev, prev = curr
4     | 4      | 3      | 5          | curr.next = prev, prev = curr
5     | 5      | 4      | None       | curr.next = prev, prev = curr
Reversed list head: 5
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single linear pass.
- **Space Complexity:** $O(1)$ in-place iterative pointer manipulation.

### Follow-Up Interview Variants
How to implement this recursively? Base case: if `head is None or head.next is None`, return `head`. Recursive step: `new_head = reverse_list(head.next); head.next.next = head; head.next = None; return new_head` ($O(N)$ stack space).

---

## Problem 24: Merge Two Sorted Lists (Easy - Linked List)

### Problem Statement
You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists into one sorted list by splicing together the nodes of the first two lists. Return the head of the merged linked list.

### Brute Force Approach & Complexity
Dump all elements into an array, sort the array, and create a new linked list. Time: $O((N + M) \log(N + M))$, Space: $O(N + M)$.

### Key Insight ("Aha!" Moment)
Use a `dummy` pre-head node and a pointer `tail`. Repeatedly attach whichever node has the smaller value (`tail.next = list1` or `list2`) in strictly $O(N + M)$ time and $O(1)$ memory.

### Optimal Python Solution
```python
def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """Merges two sorted linked lists in O(N + M) time, O(1) space."""
    dummy = ListNode(0)
    tail = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
        
    tail.next = list1 if list1 else list2
    return dummy.next
```

### Edge-Case Asserts
```python
assert to_list(merge_two_lists(from_list([1, 2, 4]), from_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
assert to_list(merge_two_lists(from_list([]), from_list([]))) == []
assert to_list(merge_two_lists(from_list([]), from_list([0]))) == [0]
```

### Dry-Run Execution Trace
```text
Input: list1 = [1, 2, 4], list2 = [1, 3, 4]
Step  | p1 val   | p2 val   | Picked Node  | Merged Result       
-------------------------------------------------------
1     | 1        | 1        | 1            | [1]                 
2     | 2        | 1        | 1            | [1, 1]              
3     | 2        | 3        | 2            | [1, 1, 2]           
4     | 4        | 3        | 3            | [1, 1, 2, 3]        
5     | 4        | 4        | 4            | [1, 1, 2, 3, 4]     
6     | None     | 4        | 4            | [1, 1, 2, 3, 4, 4]
```

### Complexity Analysis
- **Time Complexity:** $O(N + M)$ where $N$ and $M$ are the lengths of the two lists.
- **Space Complexity:** $O(1)$ auxiliary memory by relinking existing nodes.

### Follow-Up Interview Variants
What if one list is substantially longer than the other? Attach the remainder in $O(1)$ pointer assignment without looping.

---

## Problem 25: Reorder List (Medium - Linked List)

### Problem Statement
You are given the head of a singly linked-list: $L_0 \to L_1 \to \dots \to L_{n - 1} \to L_n$. Reorder the list to: $L_0 \to L_n \to L_1 \to L_{n - 1} \to L_2 \to L_{n - 2} \dots$ in-place without modifying node values.

### Brute Force Approach & Complexity
Store all nodes in an array for random access, then rebuild pointers with two indices from front and back. Time: $O(N)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Decompose into three classic sub-problems in $O(1)$ space: 1) Find middle node with fast/slow pointers, 2) Reverse second half, 3) Interleave merge the two halves.

### Optimal Python Solution
```python
def reorder_list(head: Optional[ListNode]) -> None:
    """Reorders list in-place to L0 -> Ln -> L1 -> Ln-1 ..."""
    if not head or not head.next:
        return
        
    # 1. Find middle node
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
    # 2. Reverse second half
    second = slow.next
    slow.next = None
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
        
    # 3. Interleave two halves
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```

### Edge-Case Asserts
```python
h1 = from_list([1, 2, 3, 4])
reorder_list(h1)
assert to_list(h1) == [1, 4, 2, 3]

h2 = from_list([1, 2, 3, 4, 5])
reorder_list(h2)
assert to_list(h2) == [1, 5, 2, 4, 3]

h3 = from_list([1])
reorder_list(h3)
assert to_list(h3) == [1]
```

### Dry-Run Execution Trace
```text
Original list: [1, 2, 3, 4, 5]
Step 1: Find middle using fast/slow pointers -> middle node is 3
Step 2: Split into two halves: [1, 2, 3] and [4, 5]
Step 3: Reverse second half: [5, 4]
Step 4: Interleave two halves: 1 -> 5 -> 2 -> 4 -> 3
Result: [1, 5, 2, 4, 3]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ total across find-mid, reverse, and merge passes.
- **Space Complexity:** $O(1)$ strictly in-place pointer mutations.

### Follow-Up Interview Variants
How to test if a linked list is a Palindrome using the same building blocks? Find mid, reverse second half, compare node values from both heads, then restore list.

---

## Problem 26: Remove Nth Node From End of List (Medium - Linked List)

### Problem Statement
Given the `head` of a linked list, remove the $n^{\text{th}}$ node from the end of the list and return its head in one single pass.

### Brute Force Approach & Complexity
First pass: count length $L$. Second pass: advance to node $(L - n)$ and delete next node. Time: $O(N)$ (two passes), Space: $O(1)$.

### Key Insight ("Aha!" Moment)
Maintain two pointers with a fixed gap of $n$ nodes. Advance `fast` $n$ steps ahead. Then move both `fast` and `slow` together until `fast` reaches the end; `slow` will sit directly before the node to delete.

### Optimal Python Solution
```python
def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """Removes nth node from end of list in a single pass."""
    dummy = ListNode(0, head)
    slow = dummy
    fast = head
    
    # Advance fast by n steps
    for _ in range(n):
        if fast:
            fast = fast.next
            
    while fast:
        slow = slow.next
        fast = fast.next
        
    slow.next = slow.next.next
    return dummy.next
```

### Edge-Case Asserts
```python
assert to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
assert to_list(remove_nth_from_end(from_list([1]), 1)) == []
assert to_list(remove_nth_from_end(from_list([1, 2]), 1)) == [1]
assert to_list(remove_nth_from_end(from_list([1, 2]), 2)) == [2]
```

### Dry-Run Execution Trace
```text
Input: [1, 2, 3, 4, 5], n = 2
Dummy node (0) placed before head (1)
Fast advances 3 steps ahead of Slow:
  Fast at node 3 (idx 3), Slow at dummy (idx 0) - Gap of 3 nodes
Advance Fast and Slow together until Fast reaches None:
  Step 1: Slow at 1, Fast at 4
  Step 2: Slow at 2, Fast at 5
  Step 3: Slow at 3, Fast at None (End reached!)
Remove target: slow.next = slow.next.next (bypasses node 4)
Result: [1, 2, 3, 5]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single pass.
- **Space Complexity:** $O(1)$ constant auxiliary space.

### Follow-Up Interview Variants
Why is a dummy node essential? It cleanly handles deleting the head node without adding a special branch condition.

---

## Problem 27: Linked List Cycle (Easy - Linked List)

### Problem Statement
Given `head`, the head of a linked list, determine if the linked list has a cycle in it using $O(1)$ memory.

### Brute Force Approach & Complexity
Store visited node references in a hash set. If a node is seen again, a cycle exists. Time: $O(N)$, Space: $O(N)$ memory.

### Key Insight ("Aha!" Moment)
Floyd's Tortoise and Hare algorithm: Move `slow` by 1 step and `fast` by 2 steps. If a cycle exists, `fast` catches up to `slow` by closing the gap by 1 node per iteration.

### Optimal Python Solution
```python
def has_cycle(head: Optional[ListNode]) -> bool:
    """Detects cycle using Floyd's Tortoise and Hare algorithm in O(1) space."""
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
            
    return False
```

### Edge-Case Asserts
```python
n1, n2, n3, n4 = ListNode(3), ListNode(2), ListNode(0), ListNode(-4)
n1.next, n2.next, n3.next, n4.next = n2, n3, n4, n2
assert has_cycle(n1) is True

n_no_cycle = from_list([1, 2, 3])
assert has_cycle(n_no_cycle) is False
assert has_cycle(None) is False
```

### Dry-Run Execution Trace
```text
List: 3 -> 2 -> 0 -> -4 -> (loops back to node 2)
Step  | Slow Node  | Fast Node  | Status                   
-------------------------------------------------------
0     | 3 (idx 0)  | 3 (idx 0)  | Start                    
1     | 2 (idx 1)  | 0 (idx 2)  | Fast moved 2, Slow 1     
2     | 0 (idx 2)  | 2 (idx 1)  | Fast wrapped around      
3     | -4 (idx 3) | -4 (idx 3) | Collision detected! Cycle!
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear time.
- **Space Complexity:** $O(1)$ constant space without allocating memory.

### Follow-Up Interview Variants
How to find the exact node where the cycle begins (Linked List Cycle II)? When `slow` and `fast` collide, reset one pointer to `head`; move both 1 step at a time; their next meeting point is the cycle start.

---

## Problem 28: Merge K Sorted Lists (Hard - Linked List)

### Problem Statement
You are given an array of $k$ linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.

### Brute Force Approach & Complexity
Iteratively merge lists one by one using 2-list merge. Time: $O(k \cdot N)$ where $N$ is total number of nodes.

### Key Insight ("Aha!" Moment)
Maintain a Min-Heap of size $k$ containing the current heads of all $k$ lists. Popping the smallest element and pushing its `next` node takes $O(\log k)$ per node, yielding $O(N \log k)$ total time.

### Optimal Python Solution
```python
import heapq

def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """Merges k sorted linked lists using a min-heap in O(N log k) time."""
    dummy = ListNode(0)
    curr = dummy
    heap: list[tuple[int, int, ListNode]] = []
    
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
            
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
            
    return dummy.next
```

### Edge-Case Asserts
```python
l1 = from_list([1, 4, 5])
l2 = from_list([1, 3, 4])
l3 = from_list([2, 6])
assert to_list(merge_k_lists([l1, l2, l3])) == [1, 1, 2, 3, 4, 4, 5, 6]
assert to_list(merge_k_lists([])) == []
assert to_list(merge_k_lists([None])) == []
```

### Dry-Run Execution Trace
```text
Input lists: [[1, 4, 5], [1, 3, 4], [2, 6]]
Min-heap initialized with heads of each list: [(1, list0), (1, list1), (2, list2)]
Step  | Popped (val, list_id)     | Merged List              
------------------------------------------------------------
1     | (1, list 0)              | [1]                      
2     | (1, list 1)              | [1, 1]                   
3     | (2, list 2)              | [1, 1, 2]                
4     | (3, list 1)              | [1, 1, 2, 3]             
5     | (4, list 0)              | [1, 1, 2, 3, 4]          
6     | (4, list 1)              | [1, 1, 2, 3, 4, 4]       
7     | (5, list 0)              | [1, 1, 2, 3, 4, 4, 5]    
8     | (6, list 2)              | [1, 1, 2, 3, 4, 4, 5, 6]
```

### Complexity Analysis
- **Time Complexity:** $O(N \log k)$ where $N$ is total nodes and $k$ is number of lists.
- **Space Complexity:** $O(k)$ heap memory holding $k$ elements.

### Follow-Up Interview Variants
Could you achieve the same complexity without a heap? Yes, using Divide and Conquer: pair up and merge $k$ lists recursively like merge sort in $O(N \log k)$ time and $O(1)$ heap memory.

---

## Problem 29: Invert Binary Tree (Easy - Trees)

### Problem Statement
Given the `root` of a binary tree, invert the tree (mirror reflection), and return its root.

### Brute Force Approach & Complexity
Reconstruct tree using level-order serialization mirrored. Time: $O(N)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Post-order or pre-order recursive traversal: for every node, swap its left and right child pointers, then recursively invert both subtrees.

### Optimal Python Solution
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Inverts binary tree recursively in O(N) time."""
    if not root:
        return None
        
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```

### Edge-Case Asserts
```python
root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7, TreeNode(6), TreeNode(9)))
inverted = invert_tree(root)
assert inverted.val == 4
assert inverted.left.val == 7
assert inverted.right.val == 2
assert inverted.left.left.val == 9
assert invert_tree(None) is None
```

### Dry-Run Execution Trace
```text
Input tree: [4, 2, 7, 1, 3, 6, 9]
Step 1: Invert node 4 children -> left becomes 7, right becomes 2
Step 2: Recursively invert left subtree (root 7) -> children 6 and 9 swap to 9 and 6
Step 3: Recursively invert right subtree (root 2) -> children 1 and 3 swap to 3 and 1
Output tree: [4, 7, 2, 9, 6, 3, 1]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear time visiting all $N$ nodes.
- **Space Complexity:** $O(H)$ recursion stack space where $H$ is tree height ($O(\log N)$ balanced, $O(N)$ skewed).

### Follow-Up Interview Variants
How to solve this iteratively without recursion? Use a BFS queue: pop node, swap its children, and push both non-null children onto the queue.

---

## Problem 30: Maximum Depth of Binary Tree (Easy - Trees)

### Problem Statement
Given the `root` of a binary tree, return its maximum depth (number of nodes along the longest path from root to farthest leaf).

### Brute Force Approach & Complexity
Find all root-to-leaf paths and take the maximum length. Time: $O(N)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Depth of node $N$ equals $1 + \max(\text{depth}(N.\text{left}), \text{depth}(N.\text{right}))$. Base case: depth of `None` is 0.

### Optimal Python Solution
```python
def max_depth(root: Optional[TreeNode]) -> int:
    """Calculates maximum depth of binary tree in O(N) time."""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### Edge-Case Asserts
```python
root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert max_depth(root) == 3
assert max_depth(TreeNode(1, None, TreeNode(2))) == 2
assert max_depth(None) == 0
```

### Dry-Run Execution Trace
```text
Tree: [3, 9, 20, null, null, 15, 7]
DFS recursive calls:
  max_depth(node 15) = 1 + max(0, 0) = 1
  max_depth(node 7)  = 1 + max(0, 0) = 1
  max_depth(node 20) = 1 + max(depth(15), depth(7)) = 1 + 1 = 2
  max_depth(node 9)  = 1 + max(0, 0) = 1
  max_depth(node 3)  = 1 + max(depth(9), depth(20)) = 1 + 2 = 3
Maximum depth: 3
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ visiting every node once.
- **Space Complexity:** $O(H)$ recursion call stack space.

### Follow-Up Interview Variants
How to calculate minimum depth? Be careful with single-child nodes: if one child is `None`, depth is determined by the non-null child, not `min(0, right)`.

---

## Problem 31: Same Tree (Easy - Trees)

### Problem Statement
Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not. Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

### Brute Force Approach & Complexity
Serialize both trees with null markers into strings and compare. Time: $O(N)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Simultaneous DFS traversal: if both nodes are `None`, return `True`; if one is `None` or values differ, return `False`; recursively check both `(p.left, q.left)` and `(p.right, q.right)`.

### Optimal Python Solution
```python
def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    """Checks if two binary trees are identical in O(N) time."""
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
```

### Edge-Case Asserts
```python
t1 = TreeNode(1, TreeNode(2), TreeNode(3))
t2 = TreeNode(1, TreeNode(2), TreeNode(3))
t3 = TreeNode(1, TreeNode(2), None)
assert is_same_tree(t1, t2) is True
assert is_same_tree(t1, t3) is False
assert is_same_tree(None, None) is True
```

### Dry-Run Execution Trace
```text
Trees: p = [1, 2, 3], q = [1, 2, 3]
Step 1: Check roots: p.val (1) == q.val (1) -> True
Step 2: Check left subtrees: p.left.val (2) == q.left.val (2) -> True
Step 3: Check right subtrees: p.right.val (3) == q.right.val (3) -> True
Result: True (Both trees are structurally identical with equal values)
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ visiting every node at most once.
- **Space Complexity:** $O(H)$ recursion stack space.

### Follow-Up Interview Variants
How to test if two trees are Symmetric Mirror Trees? Compare `(p.left, q.right)` and `(p.right, q.left)` simultaneously.

---

## Problem 32: Subtree of Another Tree (Easy - Trees)

### Problem Statement
Given the roots of two binary trees `root` and `subRoot`, return `True` if there is a subtree of `root` with the same structure and node values of `subRoot` and `False` otherwise.

### Brute Force Approach & Complexity
For every node in `root`, check if the subtree starting there is identical to `subRoot` using `is_same_tree`. Time: $O(N \cdot M)$, Space: $O(H)$.

### Key Insight ("Aha!" Moment)
Traverse `root` with DFS. If `is_same_tree(root, subRoot)` is true, return `True`; otherwise, search recursively in `root.left` or `root.right`.

### Optimal Python Solution
```python
def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    """Checks if sub_root is a subtree of root."""
    def is_same(p, q):
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return is_same(p.left, q.left) and is_same(p.right, q.right)

    if not sub_root:
        return True
    if not root:
        return False
    if is_same(root, sub_root):
        return True
    return is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)
```

### Edge-Case Asserts
```python
root = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2)), TreeNode(5))
sub = TreeNode(4, TreeNode(1), TreeNode(2))
assert is_subtree(root, sub) is True
root_extra = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2, TreeNode(0))), TreeNode(5))
assert is_subtree(root_extra, sub) is False
assert is_subtree(None, None) is True
```

### Dry-Run Execution Trace
```text
Root tree: [3, 4, 5, 1, 2], Subtree: [4, 1, 2]
Step 1: Check root node (3) vs subRoot (4) -> values differ (3 != 4)
Step 2: Check left child (4) vs subRoot (4) -> values match!
Step 3: Run is_same_tree on left child: left (1) == 1, right (2) == 2 -> True
Subtree found at node 4: True
```

### Complexity Analysis
- **Time Complexity:** $O(N \cdot M)$ where $N$ and $M$ are node counts.
- **Space Complexity:** $O(H)$ recursion call stack.

### Follow-Up Interview Variants
How to achieve $O(N + M)$ strictly linear time? Serialize both trees using pre-order traversal with distinct null and delimiter tokens, then run KMP (Knuth-Morris-Pratt) string search.

---

## Problem 33: Lowest Common Ancestor of a BST (Medium - Trees)

### Problem Statement
Given a Binary Search Tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.

### Brute Force Approach & Complexity
Find root-to-node paths for both nodes and compare paths to find divergence point. Time: $O(N)$, Space: $O(H)$.

### Key Insight ("Aha!" Moment)
Exploit BST ordering property: if both values are less than `curr.val`, LCA must be in left subtree; if both are greater, LCA must be in right subtree. The moment they split (or one equals `curr.val`), `curr` is the LCA!

### Optimal Python Solution
```python
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """Finds LCA in a BST in O(H) time and O(1) space."""
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr
    return root
```

### Edge-Case Asserts
```python
r = TreeNode(6, TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))), TreeNode(8, TreeNode(7), TreeNode(9)))
assert lowest_common_ancestor(r, TreeNode(2), TreeNode(8)).val == 6
assert lowest_common_ancestor(r, TreeNode(2), TreeNode(4)).val == 2
assert lowest_common_ancestor(r, TreeNode(3), TreeNode(5)).val == 4
```

### Dry-Run Execution Trace
```text
BST Root: 6, p = 2, q = 8
Check root 6:
  p.val (2) < 6 and q.val (8) > 6
  Since p is in left subtree and q is in right subtree, paths diverge!
Lowest Common Ancestor is node 6.
```

### Complexity Analysis
- **Time Complexity:** $O(H)$ where $H$ is BST height ($O(\log N)$ balanced).
- **Space Complexity:** $O(1)$ iterative traversal.

### Follow-Up Interview Variants
What if the tree is an arbitrary Binary Tree (not a BST)? Use post-order DFS: return node if it matches $p$ or $q$; if both left and right return non-null, current node is LCA.

---

## Problem 34: Binary Tree Level Order Traversal (Medium - Trees)

### Problem Statement
Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).

### Brute Force Approach & Complexity
Calculate depth of tree, then for each depth $d$, traverse from root collecting nodes at depth $d$. Time: $O(N^2)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Use a FIFO Queue (BFS). In each iteration of the outer loop, record `level_size = len(queue)` and process exactly that many nodes to group them by layer.

### Optimal Python Solution
```python
from collections import deque

def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    """Performs level-order BFS traversal in O(N) time."""
    if not root:
        return []
        
    res = []
    q = deque([root])
    
    while q:
        level_size = len(q)
        current_level = []
        for _ in range(level_size):
            node = q.popleft()
            current_level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(current_level)
        
    return res
```

### Edge-Case Asserts
```python
root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert level_order(root) == [[3], [9, 20], [15, 7]]
assert level_order(TreeNode(1)) == [[1]]
assert level_order(None) == []
```

### Dry-Run Execution Trace
```text
Tree: [3, 9, 20, null, null, 15, 7]
Level  | Queue before level        | Extracted Level Values   
------------------------------------------------------------
0      | [3]                       | [3]                      
1      | [9, 20]                   | [9, 20]                  
2      | [15, 7]                   | [15, 7]                  
Result: [[3], [9, 20], [15, 7]]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ visiting every node exactly once.
- **Space Complexity:** $O(N)$ queue holds at most $N/2$ nodes at bottom level.

### Follow-Up Interview Variants
How to output zigzag level order traversal (alternating left-right and right-left)? Reverse alternate level lists or append to a double-ended queue using a parity flag.

---

## Problem 35: Validate Binary Search Tree (Medium - Trees)

### Problem Statement
Given the `root` of a binary tree, determine if it is a valid binary search tree (BST). A valid BST requires all left subtree values to be strictly less than node value, and all right subtree values strictly greater.

### Brute Force Approach & Complexity
Only checking `node.left.val < node.val < node.right.val` locally fails because a node deep in the left subtree could violate the root's value.

### Key Insight ("Aha!" Moment)
Pass valid value boundaries `(low, high)` down the DFS recursion. When going left, update `high = node.val`; when going right, update `low = node.val`.

### Optimal Python Solution
```python
def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Validates BST in O(N) time by propagating valid range bounds."""
    def validate(node, low=float("-inf"), high=float("inf")):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        
    return validate(root)
```

### Edge-Case Asserts
```python
valid_t = TreeNode(2, TreeNode(1), TreeNode(3))
assert is_valid_bst(valid_t) is True
invalid_t = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
assert is_valid_bst(invalid_t) is False
assert is_valid_bst(TreeNode(1, TreeNode(1))) is False # Strict inequality
assert is_valid_bst(None) is True
```

### Dry-Run Execution Trace
```text
Tree: [5, 1, 4, null, null, 3, 6]
DFS bounds checking (low, high):
  Root node 5: valid in (-inf, inf)
  Left child 1: valid in (-inf, 5)
  Right child 4: valid in (5, inf)?
    4 is NOT > 5! Invalid BST violation detected!
Result: False
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ visiting every node once.
- **Space Complexity:** $O(H)$ recursion call stack space.

### Follow-Up Interview Variants
Could this be verified using in-order traversal? Yes, an in-order traversal of a valid BST must produce a strictly increasing sequence with $prev < curr$.

---

## Problem 36: Kth Smallest Element in a BST (Medium - Trees)

### Problem Statement
Given the `root` of a binary search tree, and an integer `k`, return the $k^{\text{th}}$ smallest value (1-indexed) of all the values of the nodes in the tree.

### Brute Force Approach & Complexity
Dump all node values into an array, sort it, and return index $k-1$. Time: $O(N \log N)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
In-order traversal (`Left -> Root -> Right`) of a BST yields keys in strictly sorted ascending order. Stop early as soon as the $k^{\text{th}}$ node is visited.

### Optimal Python Solution
```python
def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """Finds kth smallest element in BST using in-order traversal."""
    stack = []
    curr = root
    
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
        
    return -1
```

### Edge-Case Asserts
```python
t1 = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
assert kth_smallest(t1, 1) == 1
t2 = TreeNode(5, TreeNode(3, TreeNode(2, TreeNode(1)), TreeNode(4)), TreeNode(6))
assert kth_smallest(t2, 3) == 3
```

### Dry-Run Execution Trace
```text
BST: [3, 1, 4, null, 2], k = 1
In-order traversal sequence (Left -> Root -> Right):
  1. Visit 1 (Smallest: count = 1 == k) -> Target reached!
Kth smallest value: 1
```

### Complexity Analysis
- **Time Complexity:** $O(H + k)$ time where $H$ is tree height.
- **Space Complexity:** $O(H)$ stack space.

### Follow-Up Interview Variants
What if the BST is modified frequently (often searched and updated)? Store the count of nodes in the left subtree at each node (Order Statistic Tree), enabling $O(H)$ lookups.

---

## Problem 37: Construct Binary Tree from Preorder and Inorder Traversal (Medium - Trees)

### Problem Statement
Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.

### Brute Force Approach & Complexity
Recursively search for root in `inorder` using linear scans: $O(N^2)$ time.

### Key Insight ("Aha!" Moment)
The first element of `preorder` is always the root. Locating this root in `inorder` splits elements into left and right subtrees. Cache `inorder` index locations in a hash map for $O(1)$ lookups, yielding $O(N)$ total time.

### Optimal Python Solution
```python
def build_tree(preorder: list[int], inorder: list[int]) -> Optional[TreeNode]:
    """Reconstructs binary tree in O(N) time using index map."""
    in_map = {val: idx for idx, val in enumerate(inorder)}
    pre_idx = 0
    
    def helper(left: int, right: int) -> Optional[TreeNode]:
        nonlocal pre_idx
        if left > right:
            return None
            
        root_val = preorder[pre_idx]
        pre_idx += 1
        root = TreeNode(root_val)
        
        mid = in_map[root_val]
        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        return root
        
    return helper(0, len(inorder) - 1)
```

### Edge-Case Asserts
```python
t = build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
assert t.val == 3
assert t.left.val == 9
assert t.right.val == 20
assert t.right.left.val == 15
assert build_tree([-1], [-1]).val == -1
assert build_tree([], []) is None
```

### Dry-Run Execution Trace
```text
Preorder: [3, 9, 20, 15, 7], Inorder: [9, 3, 15, 20, 7]
Step 1: First element of preorder is root = 3
Step 2: Find index of 3 in inorder -> index 1
  Left subtree inorder: [9] (size 1) -> preorder: [9]
  Right subtree inorder: [15, 20, 7] (size 3) -> preorder: [20, 15, 7]
Step 3: Recursively construct left child (9) and right child (20 with children 15, 7)
Result: Reconstructed root 3
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear time to build $N$ nodes.
- **Space Complexity:** $O(N)$ for hash map and recursion stack.

### Follow-Up Interview Variants
Can a binary tree be uniquely constructed from Preorder and Postorder traversals? Not in general (unless every non-leaf node has exactly two children).

---

## Problem 38: Binary Tree Maximum Path Sum (Hard - Trees)

### Problem Statement
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. Return the maximum path sum of any non-empty path.

### Brute Force Approach & Complexity
Find all pairs of nodes and sum values along the path between them. Time: $O(N^2)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
Post-order Tree DP: at each node $N$, compute $\text{left\_gain} = \max(0, \text{dfs}(N.\text{left}))$ and $\text{right\_gain} = \max(0, \text{dfs}(N.\text{right}))$. The local peak path is $N.\text{val} + \text{left\_gain} + \text{right\_gain}$. Return $N.\text{val} + \max(\text{left\_gain}, \text{right\_gain})$ to the caller.

### Optimal Python Solution
```python
def max_path_sum(root: Optional[TreeNode]) -> int:
    """Computes maximum path sum in O(N) time and O(H) space."""
    max_sum = float("-inf")
    
    def gain(node: Optional[TreeNode]) -> int:
        nonlocal max_sum
        if not node:
            return 0
            
        left_gain = max(gain(node.left), 0)
        right_gain = max(gain(node.right), 0)
        
        current_path_sum = node.val + left_gain + right_gain
        max_sum = max(max_sum, current_path_sum)
        
        return node.val + max(left_gain, right_gain)
        
    gain(root)
    return int(max_sum)
```

### Edge-Case Asserts
```python
root = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert max_path_sum(root) == 42
assert max_path_sum(TreeNode(-3)) == -3
assert max_path_sum(TreeNode(1, TreeNode(2), TreeNode(3))) == 6
```

### Dry-Run Execution Trace
```text
Tree: [-10, 9, 20, null, null, 15, 7]
Post-order traversal computing max gains:
  Node 15: gain = 15, max path through 15 = 15
  Node 7:  gain = 7,  max path through 7 = 7
  Node 20: max path through 20 = 20 + 15 + 7 = 42 (New Global Max!)
           gain to parent = 20 + max(15, 7) = 35
  Node 9:  gain = 9,  max path through 9 = 9
  Node -10: max path through -10 = -10 + 9 + 35 = 34
Global Maximum Path Sum: 42
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ visiting every node once.
- **Space Complexity:** $O(H)$ recursion call stack space.

### Follow-Up Interview Variants
What if all values in the tree are negative? Clamping gains to 0 allows the algorithm to pick the single largest negative node rather than accumulating negative sums.

---

## Problem 39: Implement Trie (Prefix Tree) (Medium - Tries)

### Problem Statement
A trie (pronounced 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. Implement `insert`, `search`, and `starts_with` methods.

### Brute Force Approach & Complexity
Store strings in a list: `insert` is $O(1)$, but `search` and `starts_with` require $O(N \cdot L)$ scans across all words.

### Key Insight ("Aha!" Moment)
Each node contains a map of child nodes `children: dict[str, TrieNode]` and boolean `is_end`. Traversal follows character edges in $O(L)$ time independent of the number of words stored.

### Optimal Python Solution
```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end: bool = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return curr.is_end

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return True
```

### Edge-Case Asserts
```python
t = Trie()
t.insert("apple")
assert t.search("apple") is True
assert t.search("app") is False
assert t.starts_with("app") is True
t.insert("app")
assert t.search("app") is True
```

### Dry-Run Execution Trace
```text
Commands: insert('apple'), search('apple'), search('app'), startsWith('app')
1. insert('apple'):
   root -> 'a' -> 'p' -> 'p' -> 'l' -> 'e' (is_end = True)
2. search('apple'): path found and is_end is True -> True
3. search('app'): path found but is_end is False -> False
4. startsWith('app'): prefix path exists -> True
```

### Complexity Analysis
- **Time Complexity:** $O(L)$ for each operation where $L$ is word length.
- **Space Complexity:** $O(N \cdot L)$ in worst case with no shared prefixes.

### Follow-Up Interview Variants
How to optimize memory in memory-constrained environments? Use a Radix Tree (Patricia Trie) which compacts non-branching paths into single multi-character edges.

---

## Problem 40: Design Add and Search Words Data Structure (Medium - Tries)

### Problem Statement
Design a data structure that supports adding new words and finding if a string matches any previously added string, where `.` can represent any letter.

### Brute Force Approach & Complexity
Maintain a list and test with regular expressions on every search query. Time: $O(N \cdot L)$ per search.

### Key Insight ("Aha!" Moment)
Store words in a Trie. For exact characters, traverse the specific child node. When encountering `.`, branch DFS across all child nodes at the current level.

### Optimal Python Solution
```python
class WordNode:
    def __init__(self):
        self.children: dict[str, WordNode] = {}
        self.is_end: bool = False

class WordDictionary:
    def __init__(self):
        self.root = WordNode()

    def add_word(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = WordNode()
            curr = curr.children[ch]
        curr.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node: WordNode, idx: int) -> bool:
            if idx == len(word):
                return node.is_end
            ch = word[idx]
            if ch != '.':
                if ch not in node.children:
                    return False
                return dfs(node.children[ch], idx + 1)
            else:
                for child in node.children.values():
                    if dfs(child, idx + 1):
                        return True
                return False
        return dfs(self.root, 0)
```

### Edge-Case Asserts
```python
wd = WordDictionary()
wd.add_word("bad")
wd.add_word("dad")
wd.add_word("mad")
assert wd.search("pad") is False
assert wd.search("bad") is True
assert wd.search(".ad") is True
assert wd.search("b..") is True
```

### Dry-Run Execution Trace
```text
Words added: 'bad', 'dad', 'mad'
Search '.ad':
  char '.' -> branch across all root children: 'b', 'd', 'm'
  Branch 'b': matches 'a' -> 'd' (is_end = True) -> Matched!
Result: True
```

### Complexity Analysis
- **Time Complexity:** $O(L)$ for `add_word`; $O(26^L)$ worst-case for search with all dots, $O(L)$ average case.
- **Space Complexity:** $O(N \cdot L)$ to store words in the Trie.

### Follow-Up Interview Variants
How to prevent worst-case exponential slowdown on searches like `"...."`? Group words by length in separate Tries or hash maps.

---

## Problem 41: Word Search II (Hard - Tries)

### Problem Statement
Given an $m \times n$ `board` of characters and a list of strings `words`, return all words on the board. Each word must be constructed from sequentially adjacent cells.

### Brute Force Approach & Complexity
Run standard Word Search I for each word in `words`. Time: $O(W \cdot M \cdot N \cdot 4^L)$.

### Key Insight ("Aha!" Moment)
Build a Trie of all target words. Run DFS on the board once, traversing the Trie simultaneously. Prune leaf nodes from the Trie when a word is discovered to optimize subsequent searches.

### Optimal Python Solution
```python
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """Finds all words on board using Trie-guided backtracking DFS."""
    trie: dict = {}
    for word in words:
        curr = trie
        for ch in word:
            curr = curr.setdefault(ch, {})
        curr["$"] = word
        
    rows, cols = len(board), len(board[0])
    res = []
    
    def dfs(r: int, c: int, parent: dict):
        ch = board[r][c]
        curr_node = parent[ch]
        
        if "$" in curr_node:
            res.append(curr_node.pop("$"))
            
        board[r][c] = "#"  # Mark visited
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in curr_node:
                dfs(nr, nc, curr_node)
        board[r][c] = ch   # Backtrack
        
        # Leaf pruning optimization
        if not curr_node:
            parent.pop(ch)
            
    for r in range(rows):
        for c in range(cols):
            if board[r][c] in trie:
                dfs(r, c, trie)
                
    return res
```

### Edge-Case Asserts
```python
b = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
w = ["oath","pea","eat","rain"]
assert sorted(find_words(b, w)) == sorted(["eat", "oath"])
b2 = [["a","b"],["c","d"]]
assert find_words(b2, ["abcd"]) == []
```

### Dry-Run Execution Trace
```text
Board: [['o','a','a','n'],['e','t','a','e'],['i','h','k','r'],['i','f','l','v']]
Words: ['oath', 'pea', 'eat', 'rain']
1. Insert words into Trie: ['oath', 'pea', 'eat', 'rain']
2. Backtrack DFS starting from board[0][0]='o':
   Trie path: 'o' -> 'a' -> 't' -> 'h' (Matched word 'oath'!)
3. Prune 'oath' from Trie to prevent duplicate matches.
Found words: ['oath', 'eat']
```

### Complexity Analysis
- **Time Complexity:** $O(M \cdot N \cdot 4^L)$ where $L$ is maximum word length.
- **Space Complexity:** $O(\sum L)$ space to store all words in Trie.

### Follow-Up Interview Variants
Why is leaf pruning crucial? Once a leaf word is found, pruning that path prevents future DFS explorations from retreading dead-end branches.

---

## Problem 42: Kth Largest Element in an Array (Medium - Heap / Priority Queue)

### Problem Statement
Given an integer array `nums` and an integer `k`, return the $k^{\text{th}}$ largest element in the array. Note that it is the $k^{\text{th}}$ largest element in sorted order, not the $k^{\text{th}}$ distinct element.

### Brute Force Approach & Complexity
Sort the entire array in descending order and return `nums[k-1]`. Time: $O(N \log N)$, Space: $O(1)$ or $O(N)$.

### Key Insight ("Aha!" Moment)
Maintain a **Min-Heap of size $k$**. As elements are processed, push to heap and pop smallest when size exceeds $k$. At the end, the root of the min-heap holds the $k^{\text{th}}$ largest element.

### Optimal Python Solution
```python
import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    """Finds kth largest element using min-heap in O(N log k) time."""
    heap: list[int] = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

### Edge-Case Asserts
```python
assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
assert find_kth_largest([1], 1) == 1
```

### Dry-Run Execution Trace
```text
Input: nums = [3, 2, 1, 5, 6, 4], k = 2
Step  | num   | Min-Heap of size k (<= 2) | Action         
-------------------------------------------------------
1     | 3     | [3]                       | Push into heap 
2     | 2     | [2, 3]                    | Push into heap 
3     | 1     | [2, 3]                    | Ignore (< top) 
4     | 5     | [3, 5]                    | Replace top 3 with 5
5     | 6     | [5, 6]                    | Replace top 5 with 6
6     | 4     | [5, 6]                    | Ignore (< top) 
Top of min-heap is 2th largest: 5
```

### Complexity Analysis
- **Time Complexity:** $O(N \log k)$ maintaining a size-$k$ heap.
- **Space Complexity:** $O(k)$ auxiliary space for the heap.

### Follow-Up Interview Variants
Can this be solved in $O(N)$ average time? Yes, using QuickSelect (Hoare's selection algorithm) with randomized partitioning.

---

## Problem 43: Find Median from Data Stream (Hard - Heap / Priority Queue)

### Problem Statement
The median is the middle value in an ordered integer list. Design a data structure that supports adding numbers from a data stream and finding the median of all elements so far.

### Brute Force Approach & Complexity
Maintain a sorted list via insertion sort. `addNum` takes $O(N)$ time; `findMedian` takes $O(1)$ time.

### Key Insight ("Aha!" Moment)
Use two heaps: a **Max-Heap** `small` for lower half and a **Min-Heap** `large` for upper half. Maintain size balance such that `0 <= len(small) - len(large) <= 1`. Then median is either root of `small` or the average of roots in $O(1)$.

### Optimal Python Solution
```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small: list[int] = []  # Max-heap (store negated numbers)
        self.large: list[int] = []  # Min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        
        # Ensure every element in small <= every element in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
            
        # Maintain size invariant: len(small) == len(large) or len(small) == len(large) + 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
```

### Edge-Case Asserts
```python
mf = MedianFinder()
mf.add_num(1)
mf.add_num(2)
assert mf.find_median() == 1.5
mf.add_num(3)
assert mf.find_median() == 2.0
```

### Dry-Run Execution Trace
```text
Stream operations: addNum(1), addNum(2), findMedian() -> 1.5, addNum(3), findMedian() -> 2.0
State breakdown:
  1. addNum(1): small(max-heap)=[-1], large(min-heap)=[] -> median = 1.0
  2. addNum(2): small=[-1], large=[2] -> sizes equal, median = (1+2)/2 = 1.5
  3. addNum(3): small=[-2, -1], large=[3] -> size 3, small has extra -> median = 2.0
```

### Complexity Analysis
- **Time Complexity:** $O(\log N)$ for `add_num`; $O(1)$ for `find_median`.
- **Space Complexity:** $O(N)$ memory to store stream elements.

### Follow-Up Interview Variants
What if all integers in stream are bounded in range $[0, 100]$? Use a frequency count array of size 101; `add_num` takes $O(1)$ and median calculation takes $O(100) = O(1)$ scans.

---

## Problem 44: Combination Sum (Medium - Backtracking)

### Problem Statement
Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. The same number may be chosen unlimited times.

### Brute Force Approach & Complexity
Generate all possible multisets up to target length and check sums. Exponential: $O(2^N)$ or worse.

### Key Insight ("Aha!" Moment)
Depth-First Search (DFS) Backtracking: at index $i$, either include `candidates[i]` (staying at index $i$ to allow reuse) or advance to $i+1$ (exclude `candidates[i]`). Prune when `current_sum > target`.

### Optimal Python Solution
```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """Finds all unique combinations that sum to target using backtracking."""
    res: list[list[int]] = []
    
    def backtrack(start: int, comb: list[int], remain: int):
        if remain == 0:
            res.append(list(comb))
            return
        if remain < 0:
            return
            
        for i in range(start, len(candidates)):
            comb.append(candidates[i])
            backtrack(i, comb, remain - candidates[i])
            comb.pop()
            
    backtrack(0, [], target)
    return res
```

### Edge-Case Asserts
```python
assert sorted(combination_sum([2, 3, 6, 7], 7)) == [[2, 2, 3], [7]]
assert sorted(combination_sum([2, 3, 5], 8)) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
assert combination_sum([2], 1) == []
```

### Dry-Run Execution Trace
```text
Input: candidates = [2, 3, 6, 7], target = 7
Backtracking exploration tree:
  Path [2, 2, 2]: remaining = 1 (< 2 -> backtrack)
  Path [2, 2, 3]: remaining = 0 -> Matched [2, 2, 3]!
  Path [2, 3]: remaining = 2 (< 3 for branch -> backtrack)
  Path [7]: remaining = 0 -> Matched [7]!
Unique combinations summing to 7: [[2, 2, 3], [7]]
```

### Complexity Analysis
- **Time Complexity:** $O(N^{\frac{T}{M}})$ where $T$ is target and $M$ is minimal candidate value.
- **Space Complexity:** $O(\frac{T}{M})$ recursion stack depth.

### Follow-Up Interview Variants
What if each number can be used at most once and duplicates exist in candidates (Combination Sum II)? Sort candidates and skip adjacent duplicates: `if i > start and candidates[i] == candidates[i-1]: continue`.

---

## Problem 45: Word Search (Medium - Backtracking)

### Problem Statement
Given an $m \times n$ grid of characters `board` and a string `word`, return `True` if `word` exists in the grid. The word can be constructed from sequentially adjacent cells horizontally or vertically. The same cell may not be used more than once.

### Brute Force Approach & Complexity
Generate all self-avoiding paths of length $L$ in the grid: $O(M \cdot N \cdot 4^L)$.

### Key Insight ("Aha!" Moment)
Explore with Backtracking DFS. In-place mark visited cell by temporarily setting `board[r][c] = '#'` and restoring it on backtracking. Terminate immediately upon full word match.

### Optimal Python Solution
```python
def exist(board: list[list[str]], word: str) -> bool:
    """Checks if word exists on board using DFS backtracking."""
    rows, cols = len(board), len(board[0])
    
    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False
            
        temp = board[r][c]
        board[r][c] = "#"
        
        found = (dfs(r + 1, c, idx + 1) or
                 dfs(r - 1, c, idx + 1) or
                 dfs(r, c + 1, idx + 1) or
                 dfs(r, c - 1, idx + 1))
                 
        board[r][c] = temp
        return found
        
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

### Edge-Case Asserts
```python
b = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
assert exist(b, "ABCCED") is True
assert exist(b, "SEE") is True
assert exist(b, "ABCB") is False
```

### Dry-Run Execution Trace
```text
Board: [['A', 'B', 'C', 'E'], ['S', 'F', 'C', 'S'], ['A', 'D', 'E', 'E']]
Target word: 'ABCCED'
DFS search steps:
  Start at (0, 0) 'A' -> matched char 0
  Move right to (0, 1) 'B' -> matched char 1
  Move right to (0, 2) 'C' -> matched char 2
  Move down to (1, 2) 'C' -> matched char 3
  Move down to (2, 2) 'E' -> matched char 4
  Move left to (2, 1) 'D' -> matched char 5 (Word complete!)
Result: True
```

### Complexity Analysis
- **Time Complexity:** $O(M \cdot N \cdot 3^L)$ because after the initial step we do not turn backwards.
- **Space Complexity:** $O(L)$ recursion call stack space where $L$ is word length.

### Follow-Up Interview Variants
How to prune searches before starting? Count character frequencies in the board vs `word`. If the board lacks sufficient frequency for any character, return `False` immediately.

---

## Problem 46: Subsets (Medium - Backtracking)

### Problem Statement
Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.

### Brute Force Approach & Complexity
Iterate through integers $0$ to $2^N - 1$, taking the $j^{\text{th}}$ element if the $j^{\text{th}}$ bit is set. Time: $O(N \cdot 2^N)$, Space: $O(N \cdot 2^N)$.

### Key Insight ("Aha!" Moment)
At each step in Backtracking DFS, either include `nums[i]` or exclude `nums[i]`, generating all $2^N$ subsets systematically.

### Optimal Python Solution
```python
def subsets(nums: list[int]) -> list[list[int]]:
    """Generates power set of nums in O(N * 2^N) time."""
    res: list[list[int]] = []
    subset: list[int] = []
    
    def dfs(i: int):
        if i >= len(nums):
            res.append(list(subset))
            return
            
        # Decision 1: Include nums[i]
        subset.append(nums[i])
        dfs(i + 1)
        
        # Decision 2: Do NOT include nums[i]
        subset.pop()
        dfs(i + 1)
        
    dfs(0)
    return res
```

### Edge-Case Asserts
```python
assert sorted([sorted(s) for s in subsets([1, 2, 3])]) == sorted([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])
assert subsets([0]) == [[0], []] or subsets([0]) == [[], [0]]
assert subsets([]) == [[]]
```

### Dry-Run Execution Trace
```text
Input: [1, 2, 3]
Power Set construction tree (Include / Exclude):
  Start: []
  Include 1: [1]
    Include 2: [1, 2] -> Include 3: [1, 2, 3], Exclude 3: [1, 2]
    Exclude 2: [1] -> Include 3: [1, 3], Exclude 3: [1]
  Exclude 1: []
    Include 2: [2] -> Include 3: [2, 3], Exclude 3: [2]
    Exclude 2: [] -> Include 3: [3], Exclude 3: []
Total subsets (2^3 = 8): [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
```

### Complexity Analysis
- **Time Complexity:** $O(N \cdot 2^N)$ to generate $2^N$ subsets of average length $N/2$.
- **Space Complexity:** $O(N)$ recursion depth.

### Follow-Up Interview Variants
What if the input contains duplicates (Subsets II)? Sort the array first and skip duplicate branches when excluding the current element.

---

## Problem 47: Number of Islands (Medium - Graphs)

### Problem Statement
Given an $m \times n$ 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

### Brute Force Approach & Complexity
Find all land cells and compute connected components via an $O((M \cdot N)^2)$ all-pairs reachability scan.

### Key Insight ("Aha!" Moment)
Iterate through grid. Whenever a `'1'` is found, increment island count and flood-fill sink all connected land cells to `'0'` using BFS or DFS.

### Optimal Python Solution
```python
def num_islands(grid: list[list[str]]) -> int:
    """Counts islands by sinking connected land in O(M * N) time."""
    if not grid:
        return 0
        
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def dfs(r: int, c: int):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # Sink land
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                dfs(r, c)
                
    return islands
```

### Edge-Case Asserts
```python
g1 = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
assert num_islands(g1) == 1

g2 = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
assert num_islands(g2) == 3
assert num_islands([]) == 0
```

### Dry-Run Execution Trace
```text
Input grid (4x5):
  Row 0: 1 1 0 0 0
  Row 1: 1 1 0 0 0
  Row 2: 0 0 1 0 0
  Row 3: 0 0 0 1 1
Traversal execution:
  Encounter '1' at (0, 0) -> Island 1 found! Sink connected '1's via DFS: (0,0), (0,1), (1,0), (1,1)
  Encounter '1' at (2, 2) -> Island 2 found! Sink (2, 2)
  Encounter '1' at (3, 3) -> Island 3 found! Sink (3, 3), (3, 4)
Total islands: 3
```

### Complexity Analysis
- **Time Complexity:** $O(M \cdot N)$ visiting every cell a constant number of times.
- **Space Complexity:** $O(M \cdot N)$ worst-case call stack space for a grid filled with land.

### Follow-Up Interview Variants
What if mutating the input grid is forbidden? Maintain a `visited` boolean set/matrix or use Disjoint Set Union (Union-Find).

---

## Problem 48: Clone Graph (Medium - Graphs)

### Problem Statement
Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in the graph contains a value (`int`) and a list (`List[Node]`) of its neighbors.

### Brute Force Approach & Complexity
Traversing without tracking visited nodes causes an infinite loop due to graph cycles.

### Key Insight ("Aha!" Moment)
Maintain a hash map `visited: dict[Node, Node]` mapping original node references to their cloned copies. For each neighbor, either recurse or return the existing clone from the map.

### Optimal Python Solution
```python
class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node: Optional[GraphNode]) -> Optional[GraphNode]:
    """Clones an undirected graph using DFS in O(V + E) time."""
    if not node:
        return None
        
    cloned: dict[GraphNode, GraphNode] = {}
    
    def dfs(curr: GraphNode) -> GraphNode:
        if curr in cloned:
            return cloned[curr]
            
        copy = GraphNode(curr.val)
        cloned[curr] = copy
        for nei in curr.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy
        
    return dfs(node)
```

### Edge-Case Asserts
```python
n1 = GraphNode(1)
n2 = GraphNode(2)
n1.neighbors.append(n2)
n2.neighbors.append(n1)

c1 = clone_graph(n1)
assert c1 is not n1
assert c1.val == 1
assert len(c1.neighbors) == 1
assert c1.neighbors[0].val == 2
assert c1.neighbors[0].neighbors[0] is c1
assert clone_graph(None) is None
```

### Dry-Run Execution Trace
```text
Graph: 1 -- 2, 2 -- 3, 3 -- 4, 4 -- 1 (Cycle of 4 nodes)
DFS clone process:
  1. Visit node 1 -> Create clone Node(1), store in visited map
  2. Visit neighbor 2 -> Create clone Node(2), link clone(1).neighbors.append(clone(2))
  3. Visit neighbor 3 -> Create clone Node(3)
  4. Visit neighbor 4 -> Create clone Node(4)
  5. Node 4 points back to 1 -> clone(1) already in visited map! Link without recurse.
Result: Deep copy created with identical topology and separate memory references.
```

### Complexity Analysis
- **Time Complexity:** $O(V + E)$ visiting every vertex and edge once.
- **Space Complexity:** $O(V)$ hash map memory to store vertex clones.

### Follow-Up Interview Variants
How to implement this with BFS instead of DFS? Use a queue: pop node, iterate neighbors, clone unvisited neighbors, push to queue, and wire up neighbor pointers.

---

## Problem 49: Pacific Atlantic Water Flow (Medium - Graphs)

### Problem Statement
There is an $m \times n$ rectangular island that borders both the Pacific Ocean (top and left edges) and Atlantic Ocean (bottom and right edges). Water flows from a cell to an adjacent cell with an equal or lower height. Return a list of grid coordinates where water can flow to both oceans.

### Brute Force Approach & Complexity
Run BFS/DFS from every cell $(r, c)$ to check if both oceans are reachable. Time: $O((M \cdot N)^2)$.

### Key Insight ("Aha!" Moment)
Reverse the problem: start from the ocean borders and simulate water flowing **uphill** ($h[\text{next}] \ge h[\text{curr}]$). Cells in the intersection of both reachability sets flow to both oceans.

### Optimal Python Solution
```python
def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    """Finds cells that can reach both oceans via reverse uphill BFS/DFS."""
    if not heights:
        return []
        
    rows, cols = len(heights), len(heights[0])
    pac, atl = set(), set()
    
    def dfs(r: int, c: int, visit: set):
        visit.add((r, c))
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visit:
                if heights[nr][nc] >= heights[r][c]:  # Reverse flow: uphill
                    dfs(nr, nc, visit)
                    
    for c in range(cols):
        dfs(0, c, pac)
        dfs(rows - 1, c, atl)
    for r in range(rows):
        dfs(r, 0, pac)
        dfs(r, cols - 1, atl)
        
    return [list(coord) for coord in (pac & atl)]
```

### Edge-Case Asserts
```python
h = [
  [1,2,2,3,5],
  [3,2,3,4,4],
  [2,4,5,3,1],
  [6,7,1,4,5],
  [5,1,1,2,4]
]
res = pacific_atlantic(h)
assert sorted(res) == sorted([[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]])
assert pacific_atlantic([[1]]) == [[0, 0]]
```

### Dry-Run Execution Trace
```text
Grid (5x5 elevation map):
  Pacific borders: Top and Left edges
  Atlantic borders: Bottom and Right edges
Reverse inward flow search:
  1. Multi-source BFS/DFS from Pacific boundary uphill (height >= prev): marks pacific_reachable set
  2. Multi-source BFS/DFS from Atlantic boundary uphill: marks atlantic_reachable set
  3. Intersection pacific_reachable & atlantic_reachable yields cells that flow to both oceans.
Example coordinates: [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
```

### Complexity Analysis
- **Time Complexity:** $O(M \cdot N)$ as each cell is visited at most twice.
- **Space Complexity:** $O(M \cdot N)$ memory for reachability sets.

### Follow-Up Interview Variants
What if water can flow diagonally as well? Add 4 diagonal vectors to the exploration directions without changing the algorithmic structure.

---

## Problem 50: Course Schedule (Medium - Graphs)

### Problem Statement
There are a total of `numCourses` courses you have to take, labeled from $0$ to $\text{numCourses} - 1$. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates that you must take course $b$ first if you want to take course $a$. Return `True` if you can finish all courses.

### Brute Force Approach & Complexity
Exhaustively check all permutations of course sequences: $O(N!)$.

### Key Insight ("Aha!" Moment)
This is directed graph cycle detection. Use **Kahn's Algorithm (BFS with In-Degrees)**: start with in-degree 0 nodes; decrement neighbor in-degrees on pop. If the number of processed nodes equals `numCourses`, no cycle exists.

### Optimal Python Solution
```python
from collections import deque

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """Determines if all courses can be finished using topological sort."""
    adj: list[list[int]] = [[] for _ in range(num_courses)]
    in_degrees = [0] * num_courses
    
    for crs, pre in prerequisites:
        adj[pre].append(crs)
        in_degrees[crs] += 1
        
    queue = deque([i for i in range(num_courses) if in_degrees[i] == 0])
    count = 0
    
    while queue:
        node = queue.popleft()
        count += 1
        for nei in adj[node]:
            in_degrees[nei] -= 1
            if in_degrees[nei] == 0:
                queue.append(nei)
                
    return count == num_courses
```

### Edge-Case Asserts
```python
assert can_finish(2, [[1, 0]]) is True
assert can_finish(2, [[1, 0], [0, 1]]) is False # Cycle deadlock
assert can_finish(1, []) is True
assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True
```

### Dry-Run Execution Trace
```text
Input: numCourses = 4, prereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]
Graph construction:
  In-degrees: {0: 0, 1: 1, 2: 1, 3: 2}
  Adjacency: 0 -> [1, 2], 1 -> [3], 2 -> [3]
Kahn's BFS queue simulation:
  Step 1: In-degree 0 courses -> Queue: [0]
  Step 2: Pop 0 (courses_taken = 1). Decrement neighbors 1 and 2 -> In-degrees: {1: 0, 2: 0} -> Queue: [1, 2]
  Step 3: Pop 1 (courses_taken = 2). Decrement 3 -> In-degree: {3: 1}
  Step 4: Pop 2 (courses_taken = 3). Decrement 3 -> In-degree: {3: 0} -> Queue: [3]
  Step 5: Pop 3 (courses_taken = 4). Queue empty.
Courses taken (4) == numCourses (4) -> True (DAG has no cycle)
```

### Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V = \text{numCourses}$ and $E = \text{len}(\text{prerequisites})$.
- **Space Complexity:** $O(V + E)$ adjacency list and in-degree table.

### Follow-Up Interview Variants
How to return the valid course sequence order (Course Schedule II)? Append each popped node to an `order` list; return `order` if `len(order) == numCourses` else `[]`.

---

## Problem 51: Number of Connected Components in an Undirected Graph (Medium - Graphs)

### Problem Statement
You have a graph of $n$ nodes. You are given an integer $n$ and an array `edges` where `edges[i] = [a, b]` indicates that there is an edge between $a$ and $b$ in the graph. Return the number of connected components in the graph.

### Brute Force Approach & Complexity
Adjacency list with DFS from every unvisited node. Time: $O(V + E)$, Space: $O(V + E)$.

### Key Insight ("Aha!" Moment)
Use **Disjoint Set Union (DSU)** with path compression and union-by-rank. Start with $n$ components; each successful union of two disjoint roots decrements the component count by 1 in nearly $O(1)$ amortized time ($O(\alpha(N))$).

### Optimal Python Solution
```python
def count_components(n: int, edges: list[list[int]]) -> int:
    """Counts connected components using Disjoint Set Union (Union-Find)."""
    parent = list(range(n))
    rank = [1] * n
    
    def find(p: int) -> int:
        while p != parent[p]:
            parent[p] = parent[parent[p]]  # Path compression
            p = parent[p]
        return p
        
    def union(p1: int, p2: int) -> int:
        r1, r2 = find(p1), find(p2)
        if r1 == r2:
            return 0
        if rank[r1] < rank[r2]:
            parent[r1] = r2
            rank[r2] += rank[r1]
        else:
            parent[r2] = r1
            rank[r1] += rank[r2]
        return 1
        
    components = n
    for n1, n2 in edges:
        components -= union(n1, n2)
        
    return components
```

### Edge-Case Asserts
```python
assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
assert count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
assert count_components(4, []) == 4
```

### Dry-Run Execution Trace
```text
Input: n = 5, edges = [[0, 1], [1, 2], [3, 4]]
Initial state: 5 isolated components [0], [1], [2], [3], [4]
Disjoint Set Union (DSU) operations:
  Union(0, 1): root(0) != root(1) -> Merge! Components remaining: 4
  Union(1, 2): root(0) != root(2) -> Merge! Components remaining: 3
  Union(3, 4): root(3) != root(4) -> Merge! Components remaining: 2
Final connected component count: 2 (Components: {0, 1, 2} and {3, 4})
```

### Complexity Analysis
- **Time Complexity:** $O(V + E \cdot \alpha(V))$ nearly linear time where $\alpha$ is inverse Ackermann function.
- **Space Complexity:** $O(V)$ parent and rank arrays.

### Follow-Up Interview Variants
When is DSU preferable over BFS/DFS? DSU excels in dynamic connectivity where edges arrive continuously over time (online graph connectivity).

---

## Problem 52: Graph Valid Tree (Medium - Graphs)

### Problem Statement
Given $n$ nodes labeled from $0$ to $n - 1$ and a list of undirected edges, write a function to check whether these edges make up a valid tree.

### Brute Force Approach & Complexity
DFS to check if graph is connected and has no cycles. Time: $O(V + E)$.

### Key Insight ("Aha!" Moment)
A graph of $n$ nodes is a valid tree if and only if: 1) It has exactly $n - 1$ edges, and 2) It is fully connected (no cycles). With Union-Find, if `find(u) == find(v)` on any edge, a cycle exists.

### Optimal Python Solution
```python
def valid_tree(n: int, edges: list[list[int]]) -> bool:
    """Checks if graph is a valid tree using Disjoint Set Union."""
    if len(edges) != n - 1:
        return False
        
    parent = list(range(n))
    
    def find(p: int) -> int:
        while p != parent[p]:
            parent[p] = parent[parent[p]]
            p = parent[p]
        return p
        
    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u == root_v:
            return False  # Cycle detected
        parent[root_u] = root_v
        
    return True
```

### Edge-Case Asserts
```python
assert valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
assert valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False # Cycle between 1, 2, 3
assert valid_tree(4, [[0, 1], [2, 3]]) is False # Disconnected
assert valid_tree(1, []) is True
```

### Dry-Run Execution Trace
```text
Input: n = 5, edges = [[0, 1], [0, 2], [0, 3], [1, 4]]
Tree properties check:
  1. Edge count condition: len(edges) == n - 1 (4 == 5 - 1 -> True)
  2. Union-Find cycle check:
     Union(0, 1): roots 0, 1 -> OK
     Union(0, 2): roots 0, 2 -> OK
     Union(0, 3): roots 0, 3 -> OK
     Union(1, 4): roots 0, 4 -> OK
No cycles detected and all nodes connected: True (Valid Tree)
```

### Complexity Analysis
- **Time Complexity:** $O(V \cdot \alpha(V))$ amortized time.
- **Space Complexity:** $O(V)$ parent array memory.

### Follow-Up Interview Variants
Why is `len(edges) == n - 1` an essential initial check? It immediately filters out under-connected graphs ($E < n - 1$) and graphs that must contain cycles ($E > n - 1$).

---

## Problem 53: Network Delay Time (Medium - Graphs)

### Problem Statement
You are given a network of $n$ nodes, labeled from $1$ to $n$. You are also given `times`, a list of travel times as directed edges `times[i] = (u, v, w)`. We will send a signal from node $k$. Return the minimum time it takes for all $n$ nodes to receive the signal. If it is impossible, return `-1`.

### Brute Force Approach & Complexity
Bellman-Ford algorithm with $V$ iterations: $O(V \cdot E)$.

### Key Insight ("Aha!" Moment)
Use **Dijkstra's Shortest Path Algorithm** with a Min-Heap: track shortest confirmed distance to each node. Pop lowest-latency frontier node, relax outgoing edges, and return the maximum distance among all nodes.

### Optimal Python Solution
```python
import heapq
from collections import defaultdict

def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """Finds time for signal to reach all nodes using Dijkstra's algorithm."""
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
        
    min_heap = [(0, k)]
    dist: dict[int, int] = {}
    
    while min_heap:
        d, u = heapq.heappop(min_heap)
        if u in dist:
            continue
        dist[u] = d
        
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(min_heap, (d + w, v))
                
    return max(dist.values()) if len(dist) == n else -1
```

### Edge-Case Asserts
```python
assert network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
assert network_delay_time([[1, 2, 1]], 2, 1) == 1
assert network_delay_time([[1, 2, 1]], 2, 2) == -1 # Unreachable node
```

### Dry-Run Execution Trace
```text
Input: times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]], n = 4, k = 2
Dijkstra's Priority Queue execution:
  Init: heap = [(0, 2)], dist = {2: 0}
  Pop (0, node 2): visit neighbors 1 (wt 1) and 3 (wt 1)
    Push (1, 1) -> dist[1] = 1
    Push (1, 3) -> dist[3] = 1
  Pop (1, node 1): no outgoing edges
  Pop (1, node 3): visit neighbor 4 (wt 1) -> Push (2, 4) -> dist[4] = 2
  Pop (2, node 4): no outgoing edges
Final distances: {2: 0, 1: 1, 3: 1, 4: 2} -> Max time to reach all nodes: 2
```

### Complexity Analysis
- **Time Complexity:** $O(E \log V)$ using binary min-heap.
- **Space Complexity:** $O(V + E)$ graph and heap storage.

### Follow-Up Interview Variants
What if edge weights could be negative? Dijkstra fails with negative weights; you must use Bellman-Ford or SPFA in $O(V \cdot E)$ time.

---

## Problem 54: Alien Dictionary (Hard - Graphs)

### Problem Statement
There is a new alien language that uses the English alphabet. Given a list of words from the alien language dictionary sorted lexicographically by the rules of this new language, derive the order of letters in this language. If the order is invalid, return `""`.

### Brute Force Approach & Complexity
Compare all pairs of words and check all permutations: factorial complexity.

### Key Insight ("Aha!" Moment)
Compare adjacent pairs of words `words[i]` and `words[i+1]`. The first differing character gives a directed edge $c_1 \to c_2$. Build graph and run Topological Sort (Kahn's or post-order DFS). If a cycle occurs (or prefix rule is violated like `"abc"` before `"ab"`), return `""`.

### Optimal Python Solution
```python
def alien_order(words: list[str]) -> str:
    """Derives alien alphabet order using topological sort."""
    adj = {c: set() for w in words for c in w}
    
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""  # Invalid prefix condition
            
        for j in range(min_len):
            if w1[j] != w2[j]:
                adj[w1[j]].add(w2[j])
                break
                
    visited: dict[str, bool] = {}  # False = in current DFS path, True = fully processed
    res = []
    
    def dfs(c: str) -> bool:
        if c in visited:
            return visited[c]
            
        visited[c] = False  # Mark in current recursion stack
        for nei in adj[c]:
            if not dfs(nei):
                return False
        visited[c] = True
        res.append(c)
        return True
        
    for c in list(adj.keys()):
        if c not in visited:
            if not dfs(c):
                return ""
                
    res.reverse()
    return "".join(res)
```

### Edge-Case Asserts
```python
assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
assert alien_order(["z", "x"]) == "zx"
assert alien_order(["z", "x", "z"]) == "" # Cycle detected
assert alien_order(["abc", "ab"]) == "" # Prefix violation
```

### Dry-Run Execution Trace
```text
Input dictionary: ['wrt', 'wrf', 'er', 'ett', 'rftt']
Extracting ordering from adjacent word prefixes:
  'wrt' vs 'wrf': 't' comes before 'f' -> Edge t -> f
  'wrf' vs 'er': 'w' comes before 'e' -> Edge w -> e
  'er' vs 'ett': 'r' comes before 't' -> Edge r -> t
  'ett' vs 'rftt': 'e' comes before 'r' -> Edge e -> r
Topological order of DAG: 'w' -> 'e' -> 'r' -> 't' -> 'f'
Result: 'wertf'
```

### Complexity Analysis
- **Time Complexity:** $O(C)$ where $C$ is total length of all words combined.
- **Space Complexity:** $O(U + E)$ where $U$ is unique characters (at most 26).

### Follow-Up Interview Variants
What if multiple valid alien alphabets exist? Any valid topological sort satisfies the problem criteria.

---

## Problem 55: Climbing Stairs (Easy - Dynamic Programming)

### Problem Statement
You are climbing a staircase. It takes $n$ steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### Brute Force Approach & Complexity
Recursively compute `climb(n-1) + climb(n-2)` without memoization. Time: $O(2^N)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
To reach step $n$, you must have come from step $n-1$ (taking 1 step) or step $n-2$ (taking 2 steps). Hence $W(n) = W(n-1) + W(n-2)$ (Fibonacci sequence) computed in $O(1)$ space.

### Optimal Python Solution
```python
def climb_stairs(n: int) -> int:
    """Calculates number of ways to climb n stairs in O(N) time, O(1) space."""
    if n <= 2:
        return n
        
    one, two = 1, 2
    for _ in range(3, n + 1):
        one, two = two, one + two
        
    return two
```

### Edge-Case Asserts
```python
assert climb_stairs(2) == 2
assert climb_stairs(3) == 3
assert climb_stairs(5) == 8
assert climb_stairs(1) == 1
```

### Dry-Run Execution Trace
```text
Input: n = 5 steps
Dynamic Programming state transition: dp[i] = dp[i-1] + dp[i-2]
Base cases: dp[1] = 1, dp[2] = 2
  i = 3: dp[3] = 1 + 2 = 3 ways
  i = 4: dp[4] = 2 + 3 = 5 ways
  i = 5: dp[5] = 3 + 5 = 8 ways
Total ways to climb 5 stairs: 8
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear time.
- **Space Complexity:** $O(1)$ constant auxiliary memory.

### Follow-Up Interview Variants
Can this be solved in $O(\log N)$ time? Yes, using Matrix Exponentiation on $\begin{pmatrix}1 & 1 \\ 1 & 0\end{pmatrix}^n$ or Binet's Fibonacci formula.

---

## Problem 56: House Robber (Medium - Dynamic Programming)

### Problem Statement
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected and will automatically contact the police if two adjacent houses were broken into on the same night. Determine the maximum amount of money you can rob tonight without alerting the police.

### Brute Force Approach & Complexity
Generate all non-adjacent subsets and take the maximum sum. Time: $O(2^N)$, Space: $O(N)$.

### Key Insight ("Aha!" Moment)
At house $i$, choose either: 1) Rob house $i$ plus max loot from house $i-2$, or 2) Skip house $i$ and keep max loot from house $i-1$. Rolling state `rob1, rob2` achieves $O(1)$ space.

### Optimal Python Solution
```python
def rob(nums: list[int]) -> int:
    """Finds max non-adjacent house loot in O(N) time, O(1) space."""
    rob1, rob2 = 0, 0
    for num in nums:
        rob1, rob2 = rob2, max(rob1 + num, rob2)
    return rob2
```

### Edge-Case Asserts
```python
assert rob([1, 2, 3, 1]) == 4
assert rob([2, 7, 9, 3, 1]) == 12
assert rob([5]) == 5
assert rob([]) == 0
```

### Dry-Run Execution Trace
```text
Input houses: [2, 7, 9, 3, 1]
House   | Val   | rob1 (prev-prev)   | rob2 (prev)     | New Max = max(rob1+val, rob2) 
--------------------------------------------------------------------------------
H0     | 2     | 0                  | 0               | max(0+2, 0) = 2
H1     | 7     | 0                  | 2               | max(0+7, 2) = 7
H2     | 9     | 2                  | 7               | max(2+9, 7) = 11
H3     | 3     | 7                  | 11              | max(7+3, 11) = 11
H4     | 1     | 11                 | 11              | max(11+1, 11) = 12
Max loot: 12
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear single pass.
- **Space Complexity:** $O(1)$ rolling variables.

### Follow-Up Interview Variants
What if houses are arranged in a tree structure (House Robber III)? Return a tuple `(rob_root, skip_root)` using post-order tree DP.

---

## Problem 57: House Robber II (Medium - Dynamic Programming)

### Problem Statement
You are a professional robber planning to rob houses along a street, but all houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Determine the maximum amount of money you can rob tonight without alerting the police.

### Brute Force Approach & Complexity
Exhaustively test all valid combinations: $O(2^N)$.

### Key Insight ("Aha!" Moment)
Since the first and last houses are adjacent, you can never rob both. Break the circle into two linear sub-problems: `rob(nums[:-1])` (exclude last house) and `rob(nums[1:])` (exclude first house), taking $\max(\text{Case A}, \text{Case B})$.

### Optimal Python Solution
```python
def rob_circular(nums: list[int]) -> int:
    """Solves circular house robber problem in O(N) time, O(1) space."""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
        
    def rob_linear(houses: list[int]) -> int:
        r1, r2 = 0, 0
        for h in houses:
            r1, r2 = r2, max(r1 + h, r2)
        return r2
        
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

### Edge-Case Asserts
```python
assert rob_circular([2, 3, 2]) == 3
assert rob_circular([1, 2, 3, 1]) == 4
assert rob_circular([1, 2, 3]) == 3
assert rob_circular([1]) == 1
```

### Dry-Run Execution Trace
```text
Input circular street: [2, 3, 2]
Because first house (2) and last house (2) are adjacent:
  Case A: Rob from houses [0..N-2] = [2, 3] -> Max loot = 3
  Case B: Rob from houses [1..N-1] = [3, 2] -> Max loot = 3
Max of both scenarios: max(3, 3) = 3
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ two linear passes.
- **Space Complexity:** $O(1)$ constant auxiliary memory.

### Follow-Up Interview Variants
What if houses are arranged in a 2D grid where adjacent houses share an edge? This becomes the Maximum Independent Set on bipartite grid graphs, solvable via Max Flow / Min Cut.

---

## Problem 58: Coin Change (Medium - Dynamic Programming)

### Problem Statement
You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.

### Brute Force Approach & Complexity
Exhaustively explore all combinations with recursive branching: $O(S^A)$ where $S$ is coin count and $A$ is amount.

### Key Insight ("Aha!" Moment)
Bottom-up Unbounded Knapsack: `dp[a]` stores minimum coins for amount $a$. Transition: `dp[a] = min(dp[a], 1 + dp[a - c])` for each coin $c \le a$.

### Optimal Python Solution
```python
def coin_change(coins: list[int], amount: int) -> int:
    """Finds minimum coins needed for amount using DP in O(amount * len(coins))."""
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != float("inf") else -1
```

### Edge-Case Asserts
```python
assert coin_change([1, 2, 5], 11) == 3
assert coin_change([2], 3) == -1
assert coin_change([1], 0) == 0
assert coin_change([2, 5, 10, 1], 27) == 4 # 10 + 10 + 5 + 2
```

### Dry-Run Execution Trace
```text
Input: coins = [1, 2, 5], amount = 11
Unbounded Knapsack DP table (min coins for amount a):
Amount   | Min Coins dp[a]    | Optimal transition       
-------------------------------------------------------
1        | 1                  | dp[1] = 1 + dp[0]
2        | 1                  | dp[2] = 1 + dp[1]
3        | 2                  | dp[3] = 1 + dp[2]
4        | 2                  | dp[4] = 1 + dp[3]
5        | 1                  | dp[5] = 1 + dp[4]
6        | 2                  | dp[6] = 1 + dp[5]
7        | 2                  | dp[7] = 1 + dp[6]
8        | 3                  | dp[8] = 1 + dp[7]
9        | 3                  | dp[9] = 1 + dp[8]
10       | 2                  | dp[10] = 1 + dp[9]
11       | 3                  | dp[11] = 1 + dp[10]
Minimum coins for amount 11: 3
```

### Complexity Analysis
- **Time Complexity:** $O(A \cdot C)$ where $A$ is target amount and $C$ is number of coin denominations.
- **Space Complexity:** $O(A)$ array of size `amount + 1`.

### Follow-Up Interview Variants
How to count the number of UNIQUE combinations that sum to amount (Coin Change II)? Iterate coins on outer loop and amounts on inner loop: `dp[a] += dp[a - c]`.

---

## Problem 59: Longest Increasing Subsequence (Medium - Dynamic Programming)

### Problem Statement
Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

### Brute Force Approach & Complexity
Classic $O(N^2)$ DP where `dp[i] = 1 + max(dp[j])` for all $j < i$ with `nums[j] < nums[i]`.

### Key Insight ("Aha!" Moment)
Patience Sorting with Binary Search: maintain array `tails` where `tails[i]` is the smallest tail element of all increasing subsequences of length $i+1$. For each `num`, binary search its insertion position in $O(\log N)$, yielding $O(N \log N)$ total time.

### Optimal Python Solution
```python
import bisect

def length_of_lis(nums: list[int]) -> int:
    """Finds length of longest increasing subsequence in O(N log N) time."""
    tails: list[int] = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)
```

### Edge-Case Asserts
```python
assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
assert length_of_lis([7, 7, 7, 7, 7]) == 1
assert length_of_lis([]) == 0
```

### Dry-Run Execution Trace
```text
Input: [10, 9, 2, 5, 3, 7, 101, 18]
Patience Sorting / Binary Search (tails array represents smallest tail of all increasing subsequences of length i+1):
num   | Binary Search Ins Pos  | tails state              
-------------------------------------------------------
10    | Insert/replace at 0      | [10]                     
9     | Insert/replace at 0      | [9]                      
2     | Insert/replace at 0      | [2]                      
5     | Insert/replace at 1      | [2, 5]                   
3     | Insert/replace at 1      | [2, 3]                   
7     | Insert/replace at 2      | [2, 3, 7]                
101   | Insert/replace at 3      | [2, 3, 7, 101]           
18    | Insert/replace at 3      | [2, 3, 7, 18]            
Length of LIS: 4
```

### Complexity Analysis
- **Time Complexity:** $O(N \log N)$ time using binary search bisection.
- **Space Complexity:** $O(N)$ space for tails array.

### Follow-Up Interview Variants
How to reconstruct the actual subsequence instead of just its length? Maintain predecessor pointers array `parent` mapping each element to its previous subsequence item.

---

## Problem 60: Word Break (Medium - Dynamic Programming)

### Problem Statement
Given a string `s` and a dictionary of strings `wordDict`, return `True` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

### Brute Force Approach & Complexity
Recursively check every prefix and test remainder: $O(2^N)$ time.

### Key Insight ("Aha!" Moment)
1D Dynamic Programming: `dp[i]` indicates whether prefix `s[:i]` can be segmented. For every index $i$ and word $w$ in dictionary, if `dp[i - len(w)]` is `True` and `s[i - len(w) : i] == w`, then `dp[i] = True`.

### Optimal Python Solution
```python
def word_break(s: str, word_dict: list[str]) -> bool:
    """Checks if string s can be segmented into words from word_dict."""
    dp = [False] * (len(s) + 1)
    dp[0] = True
    
    for i in range(1, len(s) + 1):
        for w in word_dict:
            if i >= len(w) and dp[i - len(w)]:
                if s[i - len(w) : i] == w:
                    dp[i] = True
                    break
                    
    return dp[len(s)]
```

### Edge-Case Asserts
```python
assert word_break("leetcode", ["leet", "code"]) is True
assert word_break("applepenapple", ["apple", "pen"]) is True
assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
assert word_break("", ["a"]) is True
```

### Dry-Run Execution Trace
```text
Input: s = 'leetcode', wordDict = ['leet', 'code']
1D DP Prefix matching: dp[i] is True if s[:i] can be segmented
i   | Prefix s[:i]    | dp[i]    | Matched Word   
---------------------------------------------
4   | 'leet'        | True     | Matched 'leet'
8   | 'leetcode'        | True     | Matched 'code'
Can segment string: True
```

### Complexity Analysis
- **Time Complexity:** $O(N \cdot M \cdot K)$ where $N = \text{len}(s)$, $M$ is dictionary word count, and $K$ is max word length.
- **Space Complexity:** $O(N)$ for the boolean DP array.

### Follow-Up Interview Variants
How to return all possible segmented sentences (Word Break II)? Use DFS with memoization returning list of formed sentences.

---

## Problem 61: Combination Sum IV (Medium - Dynamic Programming)

### Problem Statement
Given an array of distinct integers `nums` and a target integer `target`, return the number of possible combinations (permutations) that add up to `target`.

### Brute Force Approach & Complexity
Recursively branch over all elements on every step: $O(N^T)$.

### Key Insight ("Aha!" Moment)
Because order matters (e.g. `(1, 2)` and `(2, 1)` are distinct), this is a permutation DP. Transition: `dp[i] = sum(dp[i - num] for num in nums if i >= num)` with base case `dp[0] = 1`.

### Optimal Python Solution
```python
def combination_sum_4(nums: list[int], target: int) -> int:
    """Finds number of permutations adding up to target in O(target * len(nums))."""
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for i in range(1, target + 1):
        for num in nums:
            if i - num >= 0:
                dp[i] += dp[i - num]
                
    return dp[target]
```

### Edge-Case Asserts
```python
assert combination_sum_4([1, 2, 3], 4) == 7
assert combination_sum_4([9], 3) == 0
assert combination_sum_4([1, 2], 3) == 3 # (1,1,1), (1,2), (2,1)
assert combination_sum_4([4, 2], 0) == 1
```

### Dry-Run Execution Trace
```text
Input: nums = [1, 2, 3], target = 4
1D DP Permutation count: dp[i] = sum(dp[i - n] for n in nums)
Target sum i    | dp[i] combinations count 
---------------------------------------------
1               | 1                        
2               | 2                        
3               | 4                        
4               | 7                        
Total combinations for 4: 7
```

### Complexity Analysis
- **Time Complexity:** $O(T \cdot N)$ where $T$ is target and $N$ is array length.
- **Space Complexity:** $O(T)$ DP array of size $T+1$.

### Follow-Up Interview Variants
What if negative numbers were allowed in `nums`? Cycles of arbitrary length could sum to zero, creating infinite combinations. A maximum path length limit would be required.

---

## Problem 62: Decode Ways (Medium - Dynamic Programming)

### Problem Statement
A message containing letters from A-Z can be encoded into numbers using the mapping `'A' -> 1, 'B' -> 2, ... 'Z' -> 26`. Given a string `s` containing only digits, return the number of ways to decode it.

### Brute Force Approach & Complexity
Explore all 1-character and 2-character splits recursively: $O(2^N)$ time.

### Key Insight ("Aha!" Moment)
At index $i$, check two transitions: 1) Single digit $s[i-1]$ (valid if $\ne '0'$), adding $dp[i-1]$; 2) Two digits $s[i-2:i]$ (valid if between 10 and 26), adding $dp[i-2]$.

### Optimal Python Solution
```python
def num_decodings(s: str) -> int:
    """Calculates number of ways to decode string of digits in O(N) time."""
    if not s or s[0] == "0":
        return 0
        
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    
    for i in range(2, n + 1):
        # One digit check
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]
            
        # Two digit check
        two_digit = int(s[i - 2 : i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]
            
    return dp[n]
```

### Edge-Case Asserts
```python
assert num_decodings("12") == 2
assert num_decodings("226") == 3
assert num_decodings("06") == 0 # Leading zero cannot be decoded
assert num_decodings("10") == 1
assert num_decodings("27") == 1
```

### Dry-Run Execution Trace
```text
Input: '226'
DP decoding steps (single digit '1'-'9', double digit '10'-'26'):
  i = 0 ('2'): single valid '2' ('B') -> 1 way
  i = 1 ('2'): single '2' ('BB') or double '22' ('V') -> 2 ways
  i = 2 ('6'): single '6' ('BBF', 'VF') or double '26' ('BZ') -> 3 ways
Total decode ways: 3
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single linear pass.
- **Space Complexity:** $O(N)$ or $O(1)$ by storing only the previous two states.

### Follow-Up Interview Variants
What if `*` characters represent any digit from 1 to 9 (Decode Ways II)? Branch cases taking into account possibilities for `*` alone (9 ways) and paired with adjacent digits.

---

## Problem 63: Unique Paths (Medium - Dynamic Programming)

### Problem Statement
There is a robot on an $m \times n$ grid. The robot is initially located at the top-left corner and tries to move to the bottom-right corner. The robot can only move either down or right at any point in time. Return the number of possible unique paths.

### Brute Force Approach & Complexity
Recursive DFS moving down or right: $O(2^{m+n})$.

### Key Insight ("Aha!" Moment)
To reach cell $(r, c)$, the robot comes from above $(r-1, c)$ or left $(r, c-1)$. Transition: `dp[r][c] = dp[r-1][c] + dp[r][c-1]`. Rolling 1D array achieves $O(n)$ space.

### Optimal Python Solution
```python
def unique_paths(m: int, n: int) -> int:
    """Finds unique paths in m x n grid using 2D DP in O(m * n) time."""
    row = [1] * n
    
    for _ in range(m - 1):
        new_row = [1] * n
        for c in range(1, n):
            new_row[c] = new_row[c - 1] + row[c]
        row = new_row
        
    return row[-1]
```

### Edge-Case Asserts
```python
assert unique_paths(3, 7) == 28
assert unique_paths(3, 2) == 3
assert unique_paths(1, 1) == 1
assert unique_paths(3, 3) == 6
```

### Dry-Run Execution Trace
```text
Input grid: m = 3, n = 3
2D Grid DP table: dp[r][c] = dp[r-1][c] + dp[r][c-1]
Grid progression:
  Row 0: [1, 1, 1]
  Row 1: [1, 2, 3]
  Row 2: [1, 3, 6]
Unique paths to bottom-right (2, 2): 6
```

### Complexity Analysis
- **Time Complexity:** $O(m \cdot n)$ filling the table.
- **Space Complexity:** $O(n)$ space using a rolling single row.

### Follow-Up Interview Variants
Can this be computed in $O(m)$ without dynamic programming? Yes, using combinatorics: the robot must make exactly $(m - 1)$ down steps and $(n - 1)$ right steps, which equals $\binom{m + n - 2}{m - 1}$.

---

## Problem 64: Longest Common Subsequence (Medium - Dynamic Programming)

### Problem Statement
Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.

### Brute Force Approach & Complexity
Generate all $2^M$ subsequences of `text1` and check if they are in `text2`. Time: $O(2^M \cdot N)$.

### Key Insight ("Aha!" Moment)
2D Dynamic Programming: if characters match (`text1[i] == text2[j]`), `dp[i][j] = 1 + dp[i-1][j-1]`. Otherwise, discard one character from either string: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.

### Optimal Python Solution
```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    """Computes LCS length in O(M * N) time using 2D DP."""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    return dp[m][n]
```

### Edge-Case Asserts
```python
assert longest_common_subsequence("abcde", "ace") == 3
assert longest_common_subsequence("abc", "abc") == 3
assert longest_common_subsequence("abc", "def") == 0
assert longest_common_subsequence("", "a") == 0
```

### Dry-Run Execution Trace
```text
Input: text1 = 'abcde', text2 = 'ace'
2D DP Table dp[i][j] (length of LCS of text1[:i] and text2[:j]):
     |         a    c    e
-------------------------
     |    0    0    0    0
   a |    0    1    1    1
   b |    0    1    1    1
   c |    0    1    2    2
   d |    0    1    2    2
   e |    0    1    2    3
Longest Common Subsequence Length: 3
```

### Complexity Analysis
- **Time Complexity:** $O(M \cdot N)$ filling an $M \times N$ grid.
- **Space Complexity:** $O(M \cdot N)$ or $O(\min(M, N))$ space using rolling rows.

### Follow-Up Interview Variants
How to reconstruct the actual LCS string? Backtrack through the DP table from $(m, n)$: if characters match, prepend to string and move diagonally; else move in the direction of the larger neighbor.

---

## Problem 65: Edit Distance (Medium - Dynamic Programming)

### Problem Statement
Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`. You have three operations permitted on a word: insert a character, delete a character, or replace a character.

### Brute Force Approach & Complexity
Try all 3 operations at every character recursively: $O(3^{\max(M, N)})$.

### Key Insight ("Aha!" Moment)
Classic Levenshtein 2D DP: if characters match (`word1[i-1] == word2[j-1]`), cost is $0$: `dp[i][j] = dp[i-1][j-1]`. If they differ, take $1 + \min(\text{insert}: dp[i][j-1], \text{delete}: dp[i-1][j], \text{replace}: dp[i-1][j-1])$.

### Optimal Python Solution
```python
def min_distance(word1: str, word2: str) -> int:
    """Calculates edit distance between word1 and word2 in O(M * N) time."""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )
                
    return dp[m][n]
```

### Edge-Case Asserts
```python
assert min_distance("horse", "ros") == 3
assert min_distance("intention", "execution") == 5
assert min_distance("", "abc") == 3
assert min_distance("same", "same") == 0
```

### Dry-Run Execution Trace
```text
Input: word1 = 'horse', word2 = 'ros'
Levenshtein Distance 2D DP Table:
     |       r   o   s
-------------------------
     |   0   1   2   3
   h |   1   1   2   3
   o |   2   2   1   2
   r |   3   2   2   2
   s |   4   3   3   2
   e |   5   4   4   3
Minimum Edit Distance: 3
```

### Complexity Analysis
- **Time Complexity:** $O(M \cdot N)$ time filling the matrix.
- **Space Complexity:** $O(M \cdot N)$ or $O(\min(M, N))$ space with rolling row optimization.

### Follow-Up Interview Variants
What if character weights differ (e.g. deletion costs 2, replacement costs 3)? Modify the constants inside the `min(...)` branch accordingly.

---

## Problem 66: Partition Equal Subset Sum (Medium - Dynamic Programming)

### Problem Statement
Given an integer array `nums`, return `True` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or `False` otherwise.

### Brute Force Approach & Complexity
Generate all subsets and compare subset sums: $O(2^N)$.

### Key Insight ("Aha!" Moment)
Total sum must be even; target sum for each subset is $\text{target} = \text{total} // 2$. This is classic **0/1 Knapsack**: can we pick a subset of elements that sums exactly to `target`? Maintain a hash set of reachable sums.

### Optimal Python Solution
```python
def can_partition(nums: list[int]) -> bool:
    """Determines if array can be partitioned into two equal subsets."""
    total = sum(nums)
    if total % 2 != 0:
        return False
        
    target = total // 2
    dp = {0}
    
    for num in nums:
        next_dp = set(dp)
        for t in dp:
            if t + num == target:
                return True
            if t + num < target:
                next_dp.add(t + num)
        dp = next_dp
        
    return target in dp
```

### Edge-Case Asserts
```python
assert can_partition([1, 5, 11, 5]) is True
assert can_partition([1, 2, 3, 5]) is False
assert can_partition([2, 2]) is True
assert can_partition([1]) is False
```

### Dry-Run Execution Trace
```text
Input: [1, 5, 11, 5], total sum = 22
Target subset sum: 11
0/1 Knapsack DP (reverse set state update):
  Start reachable sums: {0}
  Process 1: {0, 1}
  Process 5: {0, 1, 5, 6}
  Process 11: {0, 1, 5, 6, 11, 12, 16, 17}
  Target 11 reached! Subset exists (e.g. [1, 5, 5] and [11])
Result: True
```

### Complexity Analysis
- **Time Complexity:** $O(N \cdot \text{target})$ pseudo-polynomial time.
- **Space Complexity:** $O(\text{target})$ space to store reachable sums up to target.

### Follow-Up Interview Variants
How to optimize space to a bitset? Represent the DP state with a single integer: `dp |= (dp << num)`; check if bit at `target` is set in $O(N \cdot \text{target} / 64)$.

---

## Problem 67: Jump Game (Medium - Dynamic Programming)

### Problem Statement
You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return `True` if you can reach the last index, or `False` otherwise.

### Brute Force Approach & Complexity
Recursively explore every jump choice from current position: $O(2^N)$.

### Key Insight ("Aha!" Moment)
Maintain the maximum index reachable so far `max_reach`. As you scan $i = 0 \dots N-1$, if $i > \text{max\_reach}$, you are stranded and cannot proceed. Otherwise, update $\text{max\_reach} = \max(\text{max\_reach}, i + nums[i])$.

### Optimal Python Solution
```python
def can_jump(nums: list[int]) -> bool:
    """Determines if last index is reachable in O(N) time, O(1) space."""
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True
```

### Edge-Case Asserts
```python
assert can_jump([2, 3, 1, 1, 4]) is True
assert can_jump([3, 2, 1, 0, 4]) is False
assert can_jump([0]) is True
assert can_jump([2, 0, 0]) is True
```

### Dry-Run Execution Trace
```text
Input: [2, 3, 1, 1, 4]
Greedy max reachable index tracker:
i   | nums[i]  | Max Reachable (max(reach, i + nums[i])) 
-------------------------------------------------------
0   | 2        | max_reach = 2
1   | 3        | max_reach = 4
2   | 1        | max_reach = 4
3   | 1        | max_reach = 4
4   | 4        | max_reach = 8
Reached destination index 4: True
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single pass over array.
- **Space Complexity:** $O(1)$ constant auxiliary memory.

### Follow-Up Interview Variants
How to compute the MINIMUM number of jumps needed to reach the end (Jump Game II)? Use BFS window intervals $[\text{curr\_end}, \text{farthest}]$ in $O(N)$ time and $O(1)$ space.

---

## Problem 68: Insert Interval (Medium - Intervals)

### Problem Statement
You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]` sorted in ascending order by `start_i`. You are also given an interval `newInterval`. Insert `newInterval` into `intervals` such that `intervals` is still sorted and non-overlapping (merge overlapping intervals if necessary).

### Brute Force Approach & Complexity
Append `newInterval` to `intervals`, sort in $O(N \log N)$, and run merge intervals.

### Key Insight ("Aha!" Moment)
Since the input is already sorted, execute in three linear phases: 1) Add all intervals ending before `newInterval.start`, 2) Merge all intervals overlapping with `newInterval`, 3) Add all intervals starting after `newInterval.end`.

### Optimal Python Solution
```python
def insert_interval(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    """Inserts and merges new_interval into sorted non-overlapping intervals in O(N)."""
    res: list[list[int]] = []
    i = 0
    n = len(intervals)
    
    # 1. Before new_interval
    while i < n and intervals[i][1] < new_interval[0]:
        res.append(intervals[i])
        i += 1
        
    # 2. Overlapping merges
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    res.append(new_interval)
    
    # 3. After new_interval
    while i < n:
        res.append(intervals[i])
        i += 1
        
    return res
```

### Edge-Case Asserts
```python
assert insert_interval([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
assert insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
assert insert_interval([], [5, 7]) == [[5, 7]]
```

### Dry-Run Execution Trace
```text
Input: intervals = [[1, 3], [6, 9]], newInterval = [2, 5]
Step 1: Intervals completely before newInterval (end < 2):
  None (interval [1, 3] overlaps since 3 >= 2)
Step 2: Merge overlapping intervals (start <= new_end):
  Merge [1, 3] with [2, 5] -> [min(1, 2), max(3, 5)] = [1, 5]
Step 3: Intervals completely after merged [1, 5] (start > 5):
  Append [6, 9]
Result: [[1, 5], [6, 9]]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single linear pass.
- **Space Complexity:** $O(N)$ output array memory.

### Follow-Up Interview Variants
Could binary search be used to find insertion positions? Yes, binary search finds start and end indices in $O(\log N)$, but splicing the array still requires $O(N)$ time.

---

## Problem 69: Merge Intervals (Medium - Intervals)

### Problem Statement
Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

### Brute Force Approach & Complexity
Graph connected components: represent intervals as nodes, overlap as edges, and find connected components. Time: $O(N^2)$.

### Key Insight ("Aha!" Moment)
Sort intervals by start time. Iterate through sorted intervals: if the current interval starts before or at the end of the previous interval (`curr[0] <= prev[1]`), merge them by extending `prev[1] = max(prev[1], curr[1])`. Otherwise, append `curr` as a new interval.

### Optimal Python Solution
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merges overlapping intervals in O(N log N) time."""
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            prev[1] = max(prev[1], current[1])
        else:
            merged.append(current)
            
    return merged
```

### Edge-Case Asserts
```python
assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
assert merge_intervals([]) == []
assert merge_intervals([[1, 4], [0, 4]]) == [[0, 4]]
```

### Dry-Run Execution Trace
```text
Input intervals (sorted): [[1, 3], [2, 6], [8, 10], [15, 18]]
Step  | Interval     | Current Merged State           | Action                   
---------------------------------------------------------------------------
1     | [1, 3]       | [[1, 3]]                       | Initial interval         
2     | [2, 6]       | [[1, 6]]                       | Overlap (2 <= 3): merge  
3     | [8, 10]      | [[1, 6], [8, 10]]              | Disjoint (8 > 6): append 
4     | [15, 18]     | [[1, 6], [8, 10], [15, 18]]    | Disjoint (15 > 10): append
Final merged intervals: [[1, 6], [8, 10], [15, 18]]
```

### Complexity Analysis
- **Time Complexity:** $O(N \log N)$ dominated by sorting.
- **Space Complexity:** $O(N)$ for output list and sorting memory.

### Follow-Up Interview Variants
What if input intervals are an unbounded data stream? Maintain an Interval Tree or Segment Tree to support dynamic insertion and merging.

---

## Problem 70: Non-overlapping Intervals (Medium - Intervals)

### Problem Statement
Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

### Brute Force Approach & Complexity
Generate all subsets of intervals and check if they are pairwise non-overlapping. Time: $O(2^N)$.

### Key Insight ("Aha!" Moment)
This is Interval Scheduling Maximization: to maximize the count of mutually compatible intervals, greedily pick intervals that **end earliest**. Sort by end time, and greedily remove any interval that starts before the previously kept interval ends.

### Optimal Python Solution
```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """Finds minimum intervals to remove for no overlaps in O(N log N) time."""
    if not intervals:
        return 0
        
    intervals.sort(key=lambda x: x[1])
    removals = 0
    prev_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            removals += 1
        else:
            prev_end = intervals[i][1]
            
    return removals
```

### Edge-Case Asserts
```python
assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2
assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0
```

### Dry-Run Execution Trace
```text
Input: [[1, 2], [2, 3], [3, 4], [1, 3]]
Greedy sort by END times: [[1, 2], [2, 3], [1, 3], [3, 4]]
Selection step:
  Pick [1, 2] (prev_end = 2)
  Pick [2, 3] (start 2 >= prev_end 2 -> compatible! prev_end = 3)
  Skip [1, 3] (start 1 < prev_end 3 -> conflict! Removed)
  Pick [3, 4] (start 3 >= prev_end 3 -> compatible! prev_end = 4)
Total intervals removed: 1
```

### Complexity Analysis
- **Time Complexity:** $O(N \log N)$ sorting time.
- **Space Complexity:** $O(1)$ auxiliary memory.

### Follow-Up Interview Variants
Why does sorting by END time work greedily while sorting by START time does not? An interval ending early leaves maximum room for future intervals.

---

## Problem 71: Meeting Rooms (Easy - Intervals)

### Problem Statement
Given an array of meeting time intervals where `intervals[i] = [start_i, end_i]`, determine if a person could attend all meetings without overlap.

### Brute Force Approach & Complexity
Compare all pairs $(i, j)$ and check if they overlap. Time: $O(N^2)$, Space: $O(1)$.

### Key Insight ("Aha!" Moment)
Sort meetings by start time. A person can attend all meetings if and only if every meeting starts after or at the exact time the previous meeting concludes (`intervals[i][0] >= intervals[i-1][1]`).

### Optimal Python Solution
```python
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    """Determines if a person can attend all meetings in O(N log N) time."""
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True
```

### Edge-Case Asserts
```python
assert can_attend_meetings([[0, 30], [5, 10], [15, 20]]) is False
assert can_attend_meetings([[7, 10], [2, 4]]) is True
assert can_attend_meetings([]) is True
assert can_attend_meetings([[1, 5], [5, 10]]) is True # Adjacent meetings permitted
```

### Dry-Run Execution Trace
```text
Input meetings sorted by start time: [[0, 30], [5, 10], [15, 20]]
Pair            | Meeting A end   | Meeting B start | Overlap?  
-------------------------------------------------------
[0, 30] vs [5, 10] | 30              | 5               | Conflict! (30 > 5)
Person cannot attend all meetings: False
```

### Complexity Analysis
- **Time Complexity:** $O(N \log N)$ sorting time.
- **Space Complexity:** $O(1)$ auxiliary space.

### Follow-Up Interview Variants
What if meeting times are given as timestamps with timezones? Convert all timestamps into UTC Unix epoch milliseconds before sorting.

---

## Problem 72: Meeting Rooms II (Medium - Intervals)

### Problem Statement
Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms required.

### Brute Force Approach & Complexity
For every minute in time, count how many meetings are active and find the peak. Time: $O(T \cdot N)$ where $T$ is time range.

### Key Insight ("Aha!" Moment)
Sort meetings by start time and maintain a **Min-Heap** of meeting end times. When a new meeting starts, check if the room with the earliest end time has freed up (`heap[0] <= meeting[0]`). If so, reuse that room; otherwise, allocate a new room.

### Optimal Python Solution
```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """Finds minimum meeting rooms needed using min-heap in O(N log N) time."""
    if not intervals:
        return 0
        
    intervals.sort(key=lambda x: x[0])
    rooms: list[int] = []  # Min-heap of end times
    
    for meeting in intervals:
        if rooms and rooms[0] <= meeting[0]:
            heapq.heappop(rooms)
        heapq.heappush(rooms, meeting[1])
        
    return len(rooms)
```

### Edge-Case Asserts
```python
assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
assert min_meeting_rooms([[7, 10], [2, 4]]) == 1
assert min_meeting_rooms([[1, 5], [2, 6], [3, 7], [4, 8]]) == 4
assert min_meeting_rooms([]) == 0
```

### Dry-Run Execution Trace
```text
Sorted meetings: [[0, 30], [5, 10], [15, 20]]
Min-heap stores end times of active meeting rooms:
Meeting      | Earliest End in Heap   | Heap State             | Action              
---------------------------------------------------------------------------
[0, 30]      | None                   | [30]                   | Allocate new room   
[5, 10]      | 30                     | [10, 30]               | Allocate new room   
[15, 20]     | 10                     | [20, 30]               | Reuse room (pop earliest)
Minimum conference rooms required: 2
```

### Complexity Analysis
- **Time Complexity:** $O(N \log N)$ time for sorting and heap operations.
- **Space Complexity:** $O(N)$ heap memory.

### Follow-Up Interview Variants
Could this be solved with the Line Sweep Algorithm? Yes, split intervals into start (+1) and end (-1) timestamp events, sort events, and track the maximum running prefix sum in $O(N \log N)$.

---

## Problem 73: Number of 1 Bits (Easy - Bit Manipulation)

### Problem Statement
Given a positive integer `n`, write a function that returns the number of set bits (1s) it has (also known as the Hamming weight).

### Brute Force Approach & Complexity
Loop through all 32 bits and count how many times `n & 1` is 1 by shifting `n >>= 1`. Takes 32 iterations.

### Key Insight ("Aha!" Moment)
**Brian Kernighan's Algorithm**: the operation `n & (n - 1)` clears the lowest set bit of `n`. Looping `while n: n &= (n - 1)` executes in exactly $O(K)$ iterations where $K$ is the number of 1-bits.

### Optimal Python Solution
```python
def hamming_weight(n: int) -> int:
    """Counts set bits in integer using Brian Kernighan's algorithm."""
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count
```

### Edge-Case Asserts
```python
assert hamming_weight(11) == 3 # 1011
assert hamming_weight(128) == 1 # 10000000
assert hamming_weight(2147483645) == 30
assert hamming_weight(0) == 0
```

### Dry-Run Execution Trace
```text
Input: n = 11 (binary: 0b1011)
Brian Kernighan's Algorithm (n &= n - 1 clears lowest set bit):
Step  | n (decimal)  | n (binary)   | n - 1 (binary)  | n & (n - 1) (binary)
-----------------------------------------------------------------
1     | 11           |       1011   |         1010    |            1010
2     | 10           |       1010   |         1001    |            1000
3     | 8            |       1000   |          111    |               0
Total set bits (Hamming Weight): 3
```

### Complexity Analysis
- **Time Complexity:** $O(K)$ where $K$ is number of set bits (at most 32 or 64 operations).
- **Space Complexity:** $O(1)$ constant auxiliary memory.

### Follow-Up Interview Variants
How does CPython / hardware implement this? Modern x86 processors have a dedicated `POPCNT` instruction that executes in 1 clock cycle.

---

## Problem 74: Counting Bits (Easy - Bit Manipulation)

### Problem Statement
Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` ($0 \le i \le n$), `ans[i]` is the number of 1's in the binary representation of `i`. Must run in $O(N)$ linear time.

### Brute Force Approach & Complexity
Compute `hamming_weight(i)` independently for each number from $0$ to $n$: $O(N \log N)$.

### Key Insight ("Aha!" Moment)
Dynamic Programming with bit shifting: right shifting $i$ by 1 (`i >> 1`) removes its least significant bit. The number of 1-bits in $i$ is simply `dp[i >> 1] + (i & 1)`.

### Optimal Python Solution
```python
def count_bits(n: int) -> list[int]:
    """Counts set bits for all integers 0 to n in linear O(N) time."""
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### Edge-Case Asserts
```python
assert count_bits(2) == [0, 1, 1]
assert count_bits(5) == [0, 1, 1, 2, 1, 2]
assert count_bits(0) == [0]
```

### Dry-Run Execution Trace
```text
Input: n = 5
Bit DP relation: dp[i] = dp[i >> 1] + (i & 1)
i   | Binary   | i >> 1   | dp[i >> 1]   | i & 1    | dp[i] 
--------------------------------------------------
1   |      1   | 0        | 0            | 1        | 1     
2   |     10   | 1        | 1            | 0        | 1     
3   |     11   | 1        | 1            | 1        | 2     
4   |    100   | 2        | 1            | 0        | 1     
5   |    101   | 2        | 1            | 1        | 2     
Result for n = 5: [0, 1, 1, 2, 1, 2]
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ linear time single pass.
- **Space Complexity:** $O(1)$ auxiliary memory (output array excluded).

### Follow-Up Interview Variants
Could you also compute this using Most Significant Bit (MSB)? Yes, `dp[i] = 1 + dp[i - offset]` where `offset` doubles whenever $i$ reaches a power of 2.

---

## Problem 75: Missing Number (Easy - Bit Manipulation)

### Problem Statement
Given an array `nums` containing $n$ distinct numbers in the range $[0, n]$, return the only number in the range that is missing from the array.

### Brute Force Approach & Complexity
Sort array in $O(N \log N)$ or use a hash set in $O(N)$ space.

### Key Insight ("Aha!" Moment)
XOR self-cancellation: $a \oplus a = 0$ and $a \oplus 0 = a$. XORing all expected numbers $0 \dots n$ with all actual numbers in `nums` causes every present number to cancel out, leaving strictly the missing number in $O(1)$ space.

### Optimal Python Solution
```python
def missing_number(nums: list[int]) -> int:
    """Finds missing number in O(N) time, O(1) space using XOR."""
    res = len(nums)
    for i, num in enumerate(nums):
        res ^= i ^ num
    return res
```

### Edge-Case Asserts
```python
assert missing_number([3, 0, 1]) == 2
assert missing_number([0, 1]) == 2
assert missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
assert missing_number([0]) == 1
```

### Dry-Run Execution Trace
```text
Input: nums = [3, 0, 1], n = 3
XOR cancellation property: a ^ a = 0 and a ^ 0 = a
Initial xor_sum = 3 (binary 0b11)
i   | nums[i]  | XOR with i and nums[i]    | Running xor_sum
-------------------------------------------------------
0   | 3        | xor ^= (0 ^ 3)           | 0 (0b0)
1   | 0        | xor ^= (1 ^ 0)           | 1 (0b1)
2   | 1        | xor ^= (2 ^ 1)           | 2 (0b10)
Missing Number: 2
```

### Complexity Analysis
- **Time Complexity:** $O(N)$ single pass over array.
- **Space Complexity:** $O(1)$ constant space without risk of integer overflow.

### Follow-Up Interview Variants
Could Gauss's summation formula $\frac{n(n+1)}{2} - \sum nums$ be used instead? Yes, though in fixed-width integers (C++/Java) XOR is safer as it eliminates integer overflow risks.

---
