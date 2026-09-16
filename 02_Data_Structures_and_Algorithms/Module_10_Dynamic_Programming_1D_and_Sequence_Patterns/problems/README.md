# Module 10 — Problem Bank

Every DP problem is four questions, always in this order:

1. **What is the state?** The minimum information identifying a subproblem.
2. **What is the transition?** How states combine.
3. **What is the base case?**
4. **What is the order?** Every state computed before it is used.

Answer those on paper before writing code and DP stops being mysterious. Get
the *state* wrong and no amount of debugging will save the transition — problem
07 is the clearest example, where the obvious single-variable state is
insufficient and you need two.

**8 problems** · Easy 1 · Medium 5 · Hard 2

---

## How to work these

```bash
cd problems
python -m pytest tests -q                 # all of this module's problems
python -m pytest tests -q -k p03          # just problem 3
```

Every problem must **fail** before you start — each stub raises
`NotImplementedError`. Fill in `pNN_<slug>.py`, not the solution file.

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Jumping to the reference solution costs you the exact skill the problem
exists to build.

When you are done, compare against `solutions/pNN_<slug>.py` — not to check the
answer, which the tests already did, but to compare *approach* and complexity.

---

## Problems

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [Climbing Stairs](p01_climb_stairs.py) | 1D DP / Fibonacci recurrence | Easy | `Time O(n), Space O(1)` |
| 02 | [House Robber](p02_house_robber.py) | 1D DP with a skip constraint | Medium | `Time O(n), Space O(1)` |
| 03 | [Coin Change (Fewest Coins)](p03_coin_change_min.py) | Unbounded knapsack DP | Medium | `Time O(amount * len(coins)), Space O(amount)` |
| 04 | [Longest Increasing Subsequence](p04_lis.py) | Patience sorting / binary search DP | Hard | `Time O(n log n), Space O(n)` |
| 05 | [Word Break](p05_word_break.py) | 1D DP over string prefixes | Medium | `Time O(n * longest_word), Space O(n)` |
| 06 | [Decode Ways](p06_decode_ways.py) | 1D DP with a two-character lookback | Medium | `Time O(n), Space O(1)` |
| 07 | [Maximum Product Subarray](p07_max_product_subarray.py) | 1D DP with two-value state | Medium | `Time O(n), Space O(1)` |
| 08 | [Best Time To Buy And Sell Stock With Cooldown](p08_stock_with_cooldown.py) | DP as a state machine | Hard | `Time O(n), Space O(1)` |

## Patterns covered

- 1D DP / Fibonacci recurrence
- 1D DP over string prefixes
- 1D DP with a skip constraint
- 1D DP with a two-character lookback
- 1D DP with two-value state
- DP as a state machine
- Patience sorting / binary search DP
- Unbounded knapsack DP

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
