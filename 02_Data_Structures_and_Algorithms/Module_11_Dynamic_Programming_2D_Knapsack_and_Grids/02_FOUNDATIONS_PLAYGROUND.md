# 🐣 Interactive Foundations Playground: 2D Dynamic Programming, Knapsack & Grids

> *"2D DP is filling out a spreadsheet where each cell is calculated from its top and left neighbors."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Grid Unique Paths Transition

Moving only down or right, paths to cell $(r, c)$ equals $\text{paths}(r-1, c) + \text{paths}(r, c-1)$.

```python
def unique_paths(m, n):
    dp = [1] * n
    for r in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]
    return dp[-1]

assert unique_paths(3, 3) == 6
assert unique_paths(1, 1) == 1
assert unique_paths(3, 7) == 28
print(f"Unique paths on 3x3 grid: {unique_paths(3, 3)}, 3x7 grid: {unique_paths(3, 7)}")
```

---

## 2. 0/1 Knapsack Decision Boundary

For each item with weight $w$ and value $v$, we decide whether to include it or exclude it, iterating backwards through capacity to reuse 1D memory.

```python
def knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for cap in range(capacity, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[capacity]

max_val = knapsack([2, 3, 4, 5], [3, 4, 5, 6], 5)
assert max_val == 7, "Items with w=2 (v=3) and w=3 (v=4) give total v=7"
assert knapsack([10], [100], 5) == 0, "Item exceeds capacity"
print(f"Max knapsack value for capacity 5: {max_val}")
```

---

## 3. Longest Common Subsequence (LCS)

If characters match, $dp[i][j] = 1 + dp[i-1][j-1]$; otherwise take the maximum of skipping either character $\max(dp[i-1][j], dp[i][j-1])$.

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

assert lcs("abcde", "ace") == 3, "Common subsequence is 'ace'"
assert lcs("abc", "def") == 0
assert lcs("ezupkr", "ubmrapg") == 2
print(f"LCS of 'abcde' and 'ace': {lcs('abcde', 'ace')}")
```

---
