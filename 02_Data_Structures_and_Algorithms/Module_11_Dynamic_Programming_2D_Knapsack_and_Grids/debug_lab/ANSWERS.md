# Debug Lab 11 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — Knapsack takes the same item more than once

**Location:** `knapsack_01`, the capacity loop direction

**The bug:**

```python
for c in range(w, capacity + 1):        # LOW to HIGH
    best[c] = max(best[c], best[c - w] + v)
```

**The fix:**

```python
# HIGH to LOW: best[c - w] is then still the value from the previous item,
# so the current item can be taken at most once.
for c in range(capacity, w - 1, -1):
    best[c] = max(best[c], best[c - w] + v)
```

**Why it matters.** Iterating capacity upward means `best[c - w]` may already include the current
item, so taking it again compounds. The recurrence quietly becomes *unbounded*
knapsack, where every item has infinite supply.

The reported value is always achievable under the looser rules and is always
greater than or equal to the correct answer — a larger, entirely plausible
number. `[1] / [10] / cap 3` returns 30 instead of 10, which reads as a
suspiciously good allocation rather than an error.

This is the single most important direction-dependency in dynamic programming.
The loop direction is not a style choice; it encodes which variant of the problem
is being solved.

**Proved by:** `test_p04_knapsack_01`

## Defect 2 — An odd total is partitioned into two equal halves

**Location:** `can_partition`, the missing parity check

**The bug:**

```python
total = sum(nums)
target = total // 2     # silently rounds an odd total down
```

**The fix:**

```python
total = sum(nums)
if total % 2 != 0:
    return False        # an odd total cannot split into two equal halves
target = total // 2
```

**Why it matters.** Integer division rounds an odd total down, so the function asks whether some
subset reaches `(total - 1) / 2` — a question with no bearing on whether the array
splits evenly. When that smaller target happens to be reachable, it reports a
partition that cannot exist.

The answer is a plausible boolean, and it is correct for every even total, which
is half of any random test set.

The parity check is one line and it is a precondition, not an optimisation: the
DP that follows is only meaningful once the target is known to be exact.

**Proved by:** `test_p05_can_partition`

## Defect 3 — Every grid path cost is far too low

**Location:** `min_path_sum`, the initialisation of the first row

**The bug:**

```python
best = list(grid[0])        # the raw row, not its running totals
```

**The fix:**

```python
# The first row has only one way in - from the left - so it must hold the
# RUNNING TOTAL, not the individual cell values.
best = [0] * cols
best[0] = grid[0][0]
for c in range(1, cols):
    best[c] = best[c - 1] + grid[0][c]
```

**Why it matters.** `best` is supposed to hold, for each column, the cost of the cheapest path
*reaching* that cell. Seeding it with the raw first row claims that every cell in
row 0 can be entered for its own value alone — but the only way into row 0 is by
walking across it from the left, paying for every cell on the way.

Every subsequent row builds on that understated baseline, so the final answer is
too low: 3 instead of 7 on the first example. It is still a positive integer of
plausible size, and there is no path that actually costs 3, so nothing downstream
can detect it.

A DP table's base case is a claim about the subproblems, not a convenient place
to copy the input. State what `best[c]` means in one sentence, then check the
initialisation against that sentence.

**Proved by:** `test_p02_min_path_sum`

## Defect 4 — The common subsequence is too short

**Location:** `lcs`, the mismatch branch

**The bug:**

```python
else:
    cur[j] = max(prev[j], prev[j - 1])      # prev[j-1] is the DIAGONAL
```

**The fix:**

```python
else:
    # prev[j]    = drop a[i-1]  (the cell above)
    # cur[j - 1] = drop b[j-1]  (the cell to the left)
    cur[j] = max(prev[j], cur[j - 1])
```

**Why it matters.** `prev[j - 1]` is the diagonal neighbour, which represents dropping a character
from *both* strings — a strictly weaker option that is never what the mismatch
case needs. The correct alternatives are the cell above and the cell to the left.

Because the diagonal is always less than or equal to the left cell, the result is
an undercount: a real common subsequence length, just not the longest. Identical
strings and single-character matches still come out right, which is why the bug
survives casual testing.

Knowing which neighbour means what is the whole skill in 2D sequence DP. Label
the three neighbours before writing the recurrence, and the mismatch branch
writes itself.

**Proved by:** `test_p06_lcs`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | Knapsack takes the same item more than once | No |
| 2 | An odd total is partitioned into two equal halves | No |
| 3 | Every grid path cost is far too low | No |
| 4 | The common subsequence is too short | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
