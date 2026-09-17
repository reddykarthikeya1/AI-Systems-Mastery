# 🐣 Interactive Foundations Playground: 1D Dynamic Programming & Sequence Patterns

> *"Dynamic Programming is remembering your past so you don't repeat your calculations."*

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

## 1. Memoization vs Tabulation Fibonacci

Naive recursive Fibonacci takes $O(2^N)$ time. Storing subproblem solutions in an array reduces time to $O(N)$ and space to $O(1)$ by keeping only the last two states.

```python
def fib(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1

assert fib(0) == 0
assert fib(1) == 1
assert fib(10) == 55
print(f"Fibonacci(10) in O(N) time: {fib(10)}")
```

---

## 2. House Robber Choice Transition

At each house $i$, you either rob house $i$ plus optimal loot from house $i-2$, or skip house $i$ and take optimal loot from $i-1$: $dp[i] = \max(dp[i-1], dp[i-2] + \text{val}[i])$.

```python
def rob(nums):
    rob1, rob2 = 0, 0
    for n in nums:
        rob1, rob2 = rob2, max(rob2, rob1 + n)
    return rob2

assert rob([1, 2, 3, 1]) == 4, "Rob house 0 (1) + house 2 (3) = 4"
assert rob([2, 7, 9, 3, 1]) == 12, "2 + 9 + 1 = 12"
assert rob([5]) == 5
print(f"Max loot for [2, 7, 9, 3, 1]: {rob([2, 7, 9, 3, 1])}")
```

---

## 3. Coin Change Minimum Count

Finding the fewest coins to make amount $A$ solves $dp[a] = 1 + \min_{c} dp[a - c]$ for all denominations $c$.

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
    return dp[amount] if dp[amount] != float('inf') else -1

assert coin_change([1, 2, 5], 11) == 3, "5 + 5 + 1 = 3 coins"
assert coin_change([2], 3) == -1, "Impossible"
assert coin_change([1], 0) == 0
print(f"Fewest coins to make 11: {coin_change([1, 2, 5], 11)}")
```

---
