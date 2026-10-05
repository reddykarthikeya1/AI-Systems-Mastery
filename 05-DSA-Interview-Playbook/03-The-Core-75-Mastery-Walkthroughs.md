# DSA Playbook Chapter 3: High-Yield Problem Walkthroughs with Visual Dry-Runs

> **Core Learning Objective:** Master high-frequency LeetCode problems through intuitive, visual walkthroughs. Learn how to transform raw problem statements into brute-force analyses, find the optimal insight, and trace execution step-by-step using a dry-run matrix.

---

## 1. Problem 1: Trapping Rain Water (Hard / Staff Level)

### The Problem:
Given $n$ non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.  
*Example:* `height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]` $\rightarrow$ **Output: 6**

### The Intuitive "Aha!" Insight:
For any single index $i$, the water trapped directly above it is determined strictly by:
$$\text{Water at } i = \max(0, \min(\text{max\_left}, \text{max\_right}) - \text{height}[i])$$
Instead of computing the left and right maximums with extra arrays ($O(N)$ space), use **Two Pointers** (`left = 0`, `right = N-1`):
* The pointer with the **smaller maximum** determines the water height! Advance that pointer inward.

```mermaid
flowchart TD
    Init["left = 0, right = N-1<br/>max_left = 0, max_right = 0"] --> Check{"height[left] < height[right]?"}
    Check -->|Yes| LeftSide["Update max_left = max(max_left, height[left])<br/>Add water: max_left - height[left]<br/>left += 1"]
    Check -->|No| RightSide["Update max_right = max(max_right, height[right])<br/>Add water: max_right - height[right]<br/>right -= 1"]
    LeftSide --> Loop{"left < right?"}
    RightSide --> Loop
    Loop -->|Yes| Check
    Loop -->|No| Done["Return total_water"]
```

### Dry-Run Matrix:
```text
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
+-----+------+-------+----------+-----------+----------------------+-------+
|Step | left | right | max_left | max_right | Water Added          | Total |
+-----+------+-------+----------+-----------+----------------------+-------+
|  1  |  0   |  11   |    0     |     1     | max_left-h[0] = 0    |   0   |
|  2  |  1   |  11   |    1     |     1     | max_right-h[11] = 0  |   0   |
|  3  |  1   |  10   |    1     |     2     | max_left-h[1] = 0    |   0   |
|  4  |  2   |  10   |    1     |     2     | max_left-h[2] = 1-0  |   1   |
|  5  |  3   |  10   |    2     |     2     | max_right-h[10] = 0  |   1   |
|  6  |  3   |   9   |    2     |     2     | max_right-h[9] = 2-1 |   2   |
... continues until pointers meet ...                                  6
```

### Optimal Python Code:
```python
def trap_rain_water(height: list[int]) -> int:
    """Computes trapped rain water in O(N) time and O(1) space."""
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

assert trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
print("Trapping Rain Water test passed!")
```

---

## 2. Problem 2: Longest Substring Without Repeating Characters

### The Problem:
Given a string `s`, find the length of the longest substring without duplicate characters.  
*Example:* `s = "abcabcbb"` $\rightarrow$ **Output: 3** ("abc")

### The Intuitive "Aha!" Insight:
Use a **Dynamic Sliding Window** (`[left, right]`):
* Maintain a hash map storing the **last seen index** of each character.
* When `s[right]` was seen inside our current window (`last_seen[char] >= left`), jump `left` directly to `last_seen[char] + 1`!

### Optimal Python Code:
```python
def length_of_longest_substring(s: str) -> int:
    """Computes longest substring without repeating characters in O(N) time, O(min(N, M)) space."""
    last_seen = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len

assert length_of_longest_substring("abcabcbb") == 3
print("Longest Substring test passed!")
```

---

## 3. Problem 3: Course Schedule (Cycle Detection in DAG)

### The Problem:
Given `numCourses` and prerequisite pairs `[a, b]` (must take $b$ before $a$), determine if it is possible to finish all courses.  
*Example:* `numCourses = 2, prerequisites = [[1, 0]]` $\rightarrow$ **Output: True**

### The Intuitive "Aha!" Insight:
This is a **Directed Cycle Detection** problem. If a cycle exists ($A \rightarrow B \rightarrow A$), you can never graduate!
* Use **Kahn's Algorithm (BFS with In-Degrees)**:
  1. Calculate `in_degree` (number of prerequisite dependencies) for every course.
  2. Put all courses with `in_degree == 0` into a queue (courses you can take immediately).
  3. Pop a course, decrement the `in_degree` of all dependent courses. If any drop to 0, push to queue.
  4. If total courses taken equals `numCourses`, return `True`!

### Optimal Python Code:
```python
from collections import deque

def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """Kahn's algorithm: O(V + E) time and O(V + E) space."""
    adj = {i: [] for i in range(num_courses)}
    in_degrees = [0] * num_courses

    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degrees[course] += 1

    queue = deque([i for i in range(num_courses) if in_degrees[i] == 0])
    courses_taken = 0

    while queue:
        curr = queue.popleft()
        courses_taken += 1

        for neighbor in adj[curr]:
            in_degrees[neighbor] -= 1
            if in_degrees[neighbor] == 0:
                queue.append(neighbor)

    return courses_taken == num_courses

assert can_finish_courses(2, [[1, 0]]) is True
assert can_finish_courses(2, [[1, 0], [0, 1]]) is False # Deadlock cycle
print("Course Schedule test passed!")
```

---

## 4. Problem 4: Design Add and Search Words Data Structure (Trie with Wildcard)

### The Problem:
Design a data structure that supports adding new words and finding if a string matches any previously added string. A query string may contain the dot character `.` to represent any one letter.  
*Example:* `addWord("bad")`, `addWord("dad")`, `addWord("mad")` $\rightarrow$ `search("pad")` is `False`, `search("bad")` is `True`, `search(".ad")` is `True`, `search("b..")` is `True`.

### The Intuitive "Aha!" Insight:
A standard hash set cannot handle wildcards without checking every stored word. A **Prefix Tree (Trie)** allows exact character lookups in $O(L)$ time. When encountering a `.`, simply fork DFS exploration across all existing children at the current node!

### [Block 1: Naive Brute Force & Big-O Failure]
```python
# JUNIOR APPROACH: List of strings with regex / linear scan
import re

class JuniorWordDictionary:
    def __init__(self):
        self.words = []

    def add_word(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        # Compiling regex and checking against every word
        pattern = re.compile("^" + word + "$")
        for stored in self.words:
            if pattern.match(stored):
                return True
        return False
# Why it breaks:
# If there are 50,000 words and 10,000 queries, this does 50,000 * 10,000 = 500,000,000 operations!
# Result: Time Limit Exceeded (TLE) in interview platforms.
```

### [Block 2: Typed Production-Optimal Implementation]
```python
from typing import Dict, Optional


class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_terminal: bool = False


class WordDictionary:
    """Trie with recursive DFS backtracking for wildcard '.' matching."""

    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        """Inserts a word into the Trie in O(L) time, where L is word length."""
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_terminal = True

    def search(self, word: str) -> bool:
        """
        Searches for word where '.' matches any character.
        Best/Average: O(L), Worst-case (all '.'): O(26^L).
        """
        def dfs(node: TrieNode, index: int) -> bool:
            if index == len(word):
                return node.is_terminal

            char = word[index]
            if char != ".":
                if char not in node.children:
                    return False
                return dfs(node.children[char], index + 1)
            else:
                # Wildcard: explore all existing child branches
                for child_node in node.children.values():
                    if dfs(child_node, index + 1):
                        return True
                return False

        return dfs(self.root, 0)
```

### [Block 3: Edge-Case Unit Tests]
```python
def test_word_dictionary():
    wd = WordDictionary()
    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")

    # Standard lookups
    assert wd.search("pad") is False, "pad should not exist"
    assert wd.search("bad") is True, "bad should exist"

    # Wildcard lookups
    assert wd.search(".ad") is True, ".ad should match bad/dad/mad"
    assert wd.search("b..") is True, "b.. should match bad"
    assert wd.search("..") is False, "Length mismatch should return False"
    assert wd.search("....") is False, "Length mismatch should return False"

    # Single character & empty word tests
    wd.add_word("a")
    assert wd.search("a") is True
    assert wd.search(".") is True
    assert wd.search("b") is False

    print("[PASS] WordDictionary (Trie Wildcard) passed all edge cases!")

test_word_dictionary()
```

---

## 5. Problem 5: Sliding Window Maximum (Monotonic Deque)

### The Problem:
Given an array of integers `nums` and a sliding window of size `k` moving from left to right, return the max element in each window.  
*Example:* `nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3` $\rightarrow$ **Output: [3, 3, 5, 5, 6, 7]**

### The Intuitive "Aha!" Insight:
When a new element $X$ enters the window, any older element in the window that is smaller than $X$ will **never again be the maximum**!
Use a **Monotonic Decreasing Deque** to store indices:
* The front of the deque always holds the index of the maximum element in the current window.
* Pop smaller elements from the back before inserting the current index.
* Pop from the front if the oldest index fell out of the window (`index <= i - k`).

### [Block 1: Naive Brute Force & Big-O Failure]
```python
# JUNIOR APPROACH: Slicing and computing max() for each window
def junior_max_sliding_window(nums: list[int], k: int) -> list[int]:
    result = []
    for i in range(len(nums) - k + 1):
        window = nums[i : i + k]
        result.append(max(window))  # max() takes O(k) time!
    return result

# Why it breaks:
# For N = 100,000 and K = 50,000, this takes O(N * K) = 5,000,000,000 operations!
# Result: Immediate TLE.
```

### [Block 2: Typed Production-Optimal Implementation]
```python
from collections import deque
from typing import List


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Computes sliding window maximum in strictly O(N) time and O(k) space
    using a monotonic decreasing double-ended queue.
    """
    if not nums or k == 0:
        return []
    if k == 1:
        return nums

    dq: deque[int] = deque()  # Stores INDICES of nums
    result: List[int] = []

    for i in range(len(nums)):
        # 1. Evict elements whose indices are outside the current window
        if dq and dq[0] <= i - k:
            dq.popleft()

        # 2. Maintain monotonic decreasing order: pop smaller elements from back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        # 3. Add current index
        dq.append(i)

        # 4. Once window reaches size k, the front is always our window maximum
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

### [Block 3: Edge-Case Unit Tests]
```python
def test_sliding_window_max():
    # Standard mixed test
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]

    # Edge Case: k equals array length (single answer)
    assert max_sliding_window([1, -1], 2) == [1]

    # Edge Case: k = 1 (every element is its own max)
    assert max_sliding_window([9, 11, 8, 5, 7], 1) == [9, 11, 8, 5, 7]

    # Edge Case: Strictly decreasing array
    assert max_sliding_window([9, 8, 7, 6, 5], 3) == [9, 8, 7]

    # Edge Case: Strictly increasing array
    assert max_sliding_window([1, 2, 3, 4, 5], 3) == [3, 4, 5]

    # Edge Case: All negative numbers
    assert max_sliding_window([-7, -8, -7, -5, -7, -3], 3) == [-7, -5, -5, -3]

    print("[PASS] Sliding Window Maximum (Monotonic Deque) passed all edge cases!")

test_sliding_window_max()
```

---

## 6. Problem 6: Binary Tree Maximum Path Sum (Tree DP)

### The Problem:
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. A node can only appear at most once in the path. Return the maximum path sum of any non-empty path.  
*Example:* `[-10, 9, 20, null, null, 15, 7]` $\rightarrow$ Path `15 -> 20 -> 7` gives **Output: 42**.

### The Intuitive "Aha!" Insight:
This is a **Post-Order Tree Dynamic Programming** problem.
At each node $N$, we decide two things:
1. **The Turn-Around Path (Local Maxima):** Can the highest path peak at $N$?  
   $\text{local\_max} = N.\text{val} + \max(0, \text{left\_gain}) + \max(0, \text{right\_gain})$. Update our global record with this.
2. **The Contribution to Parent:** If $N$ is part of a larger path continuing upward to its parent, it can only choose **ONE** child branch (either left or right)!  
   $\text{return } N.\text{val} + \max(0, \max(\text{left\_gain}, \text{right\_gain}))$.

### [Block 1: Naive Brute Force & Big-O Failure]
```python
# JUNIOR APPROACH: Find all pairs of nodes, compute path sum for each pair
# Why it breaks:
# Calculating paths between all N*(N-1)/2 pairs requires O(N^2) or O(N^3) time!
# Blows up stack recursion on trees with 30,000 nodes.
```

### [Block 2: Typed Production-Optimal Implementation]
```python
from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


class SolutionMaxPathSum:
    """
    Computes max path sum in O(N) time and O(H) recursion stack space
    using bottom-up post-order Tree Dynamic Programming.
    """

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        # Initialize to negative infinity to handle trees with all negative values
        self.global_max: float = float("-inf")

        def max_gain(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            # Post-order: compute left and right subtree contributions
            # If a subtree produces a negative sum, ignore it by clamping to 0!
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)

            # Local path sum passing through current node as the peak
            price_newpath = node.val + left_gain + right_gain

            # Update global record
            self.global_max = max(self.global_max, price_newpath)

            # Return max single-branch gain to the caller parent
            return node.val + max(left_gain, right_gain)

        max_gain(root)
        return int(self.global_max)
```

### [Block 3: Edge-Case Unit Tests]
```python
def test_max_path_sum():
    solver = SolutionMaxPathSum()

    # Standard tree: [-10, 9, 20, null, null, 15, 7] -> 15 + 20 + 7 = 42
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20, TreeNode(15), TreeNode(7))
    assert solver.maxPathSum(root) == 42

    # Edge Case: All negative values (must pick single least-negative node)
    neg_root = TreeNode(-3)
    assert solver.maxPathSum(neg_root) == -3

    neg_tree = TreeNode(-10, TreeNode(-20), TreeNode(-5))
    assert solver.maxPathSum(neg_tree) == -5

    # Edge Case: Single linear line (skewed tree)
    skewed = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert solver.maxPathSum(skewed) == 6

    print("[PASS] Binary Tree Maximum Path Sum passed all edge cases!")

test_max_path_sum()
```

---

## 7. The Complete Core 75 Master Pattern Blueprint Matrix

Every coding interview problem at Google, Meta, and Uber is a variation of these 75 core archetypes. Use this matrix to classify any interview problem within 60 seconds:

| Category | Problem Name | Primary Pattern | Target Time Complexity | Auxiliary Space |
| :--- | :--- | :--- | :---: | :---: |
| **Arrays & Hashing** | Two Sum | Hash Map (Complement) | $O(N)$ | $O(N)$ |
| | Contains Duplicate | Hash Set | $O(N)$ | $O(N)$ |
| | Valid Anagram | Frequency Count Array | $O(N)$ | $O(1)$ |
| | Group Anagrams | Character Count Key Tuple | $O(N \cdot K)$ | $O(N \cdot K)$ |
| | Top K Frequent Elements | Min-Heap or Bucket Sort | $O(N)$ | $O(N)$ |
| | Product of Array Except Self | Prefix & Suffix Products | $O(N)$ | $O(1)$ |
| | Encode and Decode Strings | Length Delimiter (`len#word`)| $O(N)$ | $O(1)$ |
| | Longest Consecutive Sequence | Hash Set + Left Boundary Check | $O(N)$ | $O(N)$ |
| **Two Pointers** | Valid Palindrome | Inward Two Pointers | $O(N)$ | $O(1)$ |
| | 3Sum | Sort + Fixed Pivot + 2 Pointers | $O(N^2)$ | $O(1)$ |
| | Container With Most Water | Two Pointers (Greedy Inward) | $O(N)$ | $O(1)$ |
| | Trapping Rain Water | Two Pointers + Running Max | $O(N)$ | $O(1)$ |
| **Sliding Window** | Best Time to Buy & Sell Stock | Running Minimum Tracker | $O(N)$ | $O(1)$ |
| | Longest Substring Without Repeats| Sliding Window + Last-Seen Map| $O(N)$ | $O(\min(N, M))$ |
| | Longest Repeating Character Replacement| Sliding Window + Max Frequency| $O(N)$ | $O(1)$ |
| | Minimum Window Substring | Sliding Window + Match Counter | $O(N + M)$ | $O(1)$ |
| **Stack** | Valid Parentheses | LIFO Stack Matching | $O(N)$ | $O(N)$ |
| | Daily Temperatures | Monotonic Decreasing Stack | $O(N)$ | $O(N)$ |
| | Largest Rectangle in Histogram | Monotonic Increasing Stack | $O(N)$ | $O(N)$ |
| **Binary Search** | Binary Search | $L \le R$ Midpoint Bisection | $O(\log N)$ | $O(1)$ |
| | Search in Rotated Sorted Array | Sorted Half Determination | $O(\log N)$ | $O(1)$ |
| | Find Minimum in Rotated Sorted Array| Rotated Inflection Bisection | $O(\log N)$ | $O(1)$ |
| **Linked List** | Reverse Linked List | 3-Pointer Iterative (`prev, curr, next`) | $O(N)$ | $O(1)$ |
| | Merge Two Sorted Lists | Dummy Head Pointer Iteration | $O(N + M)$ | $O(1)$ |
| | Reorder List | Find Mid + Reverse 2nd Half + Merge| $O(N)$ | $O(1)$ |
| | Remove Nth Node From End | Fast & Slow Pointer Gap | $O(N)$ | $O(1)$ |
| | Linked List Cycle | Floyd's Tortoise and Hare | $O(N)$ | $O(1)$ |
| | Merge K Sorted Lists | Min-Heap Priority Queue | $O(N \log K)$ | $O(K)$ |
| **Trees & Tries** | Invert Binary Tree | Recursive Post-order DFS | $O(N)$ | $O(H)$ |
| | Maximum Depth of Binary Tree | Recursive DFS | $O(N)$ | $O(H)$ |
| | Same Tree | Synchronous DFS Comparison | $O(N)$ | $O(H)$ |
| | Subtree of Another Tree | DFS Tree Traversal + SameTree | $O(N \cdot M)$ | $O(H)$ |
| | Lowest Common Ancestor (BST) | Value Bisection ($P < Root < Q$) | $O(H)$ | $O(1)$ |
| | Binary Tree Level Order Traversal | BFS with Queue (`len(q)`) | $O(N)$ | $O(N)$ |
| | Validate Binary Search Tree | DFS with Range Bounds `(low, high)`| $O(N)$ | $O(H)$ |
| | Kth Smallest Element in BST | In-order DFS (Sorted Traversal)| $O(H + K)$ | $O(H)$ |
| | Construct Tree Preorder & Inorder| Root Lookup + Subtree Bounds | $O(N)$ | $O(N)$ |
| | Binary Tree Maximum Path Sum | Post-order Max Contribution DFS | $O(N)$ | $O(H)$ |
| | Implement Trie (Prefix Tree) | Nested Dictionary Nodes | $O(L)$ | $O(N \cdot L)$ |
| | Word Search II | Trie + Backtracking DFS | $O(M \cdot 4^L)$ | $O(N \cdot L)$ |
| **Heap / PQ** | Find Median from Data Stream | Dual Heaps (Max-Heap + Min-Heap)| $O(\log N)$ add, $O(1)$ find | $O(N)$ |
| **Backtracking** | Combination Sum | Choose / Explore / Unchoose DFS | $O(2^T)$ | $O(T)$ |
| | Word Search | Grid DFS + In-place Mutation | $O(R \cdot C \cdot 4^L)$ | $O(L)$ |
| **Graphs** | Number of Islands | Grid BFS/DFS Sink Visited (`'0'`) | $O(R \cdot C)$ | $O(R \cdot C)$ |
| | Clone Graph | Hash Map Visited Clone DFS | $O(V + E)$ | $O(V)$ |
| | Pacific Atlantic Water Flow | Reverse Inward BFS from Oceans | $O(R \cdot C)$ | $O(R \cdot C)$ |
| | Course Schedule | Kahn's Topological Sort (In-Degrees)| $O(V + E)$ | $O(V + E)$ |
| | Number of Connected Components | Disjoint Set Union (DSU) | $O(V + E \cdot \alpha(V))$ | $O(V)$ |
| | Graph Valid Tree | DSU (No cycles + 1 component) | $O(V + E \cdot \alpha(V))$ | $O(V)$ |
| **Dynamic Prog.** | Climbing Stairs | Fibonacci Space Optimization | $O(N)$ | $O(1)$ |
| | Coin Change | Unbounded Knapsack (Min Coins) | $O(N \cdot A)$ | $O(A)$ |
| | Longest Increasing Subsequence | Patience Sorting + Binary Search | $O(N \log N)$ | $O(N)$ |
| | Longest Common Subsequence | 2D Grid DP (`dp[i][j]`) | $O(N \cdot M)$ | $O(\min(N, M))$ |
| | Word Break | 1D DP Prefix Dictionary Check | $O(N^2 \cdot L)$ | $O(N)$ |
| | Combination Sum IV | 1D Permutation DP | $O(T \cdot N)$ | $O(T)$ |
| | House Robber | 1D DP (`rob1, rob2` state rolling)| $O(N)$ | $O(1)$ |
| | House Robber II | Circular DP (`nums[:-1]` vs `nums[1:]`)| $O(N)$ | $O(1)$ |
| | Decode Ways | 1D DP Single vs Double Digit | $O(N)$ | $O(1)$ |
| | Unique Paths | Grid DP (Combinatorics or Rolling) | $O(R \cdot C)$ | $O(C)$ |
| | Jump Game | Greedy Max Reachable Tracker | $O(N)$ | $O(1)$ |
| **Intervals** | Insert Interval | Linear Scan (Before / Merge / After)| $O(N)$ | $O(N)$ |
| | Merge Intervals | Sort by Start Time + Linear Merge| $O(N \log N)$ | $O(N)$ |
| | Non-overlapping Intervals | Greedy Sort by End Time | $O(N \log N)$ | $O(1)$ |
| | Meeting Rooms | Sort by Start Time + Overlap Check | $O(N \log N)$ | $O(1)$ |
| | Meeting Rooms II | Min-Heap End Times or Event Sweep | $O(N \log N)$ | $O(N)$ |
| **Bit Manipulation**| Number of 1 Bits (Hamming Weight) | Brian Kernighan's Algorithm (`n & (n-1)`)| $O(\text{set bits})$ | $O(1)$ |
| | Counting Bits | DP with Most/Least Significant Bit | $O(N)$ | $O(1)$ |
| | Reverse Bits | Bitwise Shift & Masking | $O(1)$ | $O(1)$ |
| | Missing Number | XOR Cancellation (`a ^ b ^ a = b`)| $O(N)$ | $O(1)$ |
| | Sum of Two Integers | Half Adder Bitwise (`XOR` & `AND << 1`)| $O(1)$ | $O(1)$ |
