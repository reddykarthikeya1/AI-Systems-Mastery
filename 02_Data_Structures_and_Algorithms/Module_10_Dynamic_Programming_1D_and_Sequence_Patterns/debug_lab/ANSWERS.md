# Debug Lab 10 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — An impossible amount is reported as costing zero coins

**Location:** `coin_change_min`, the fallback when no coin fits

**The bug:**

```python
options = [best[a - c] + 1 for c in coins if c <= a]
best[a] = min(options) if options else 0    # 0 means 'free', not 'impossible'
```

**The fix:**

```python
INF = float("inf")
best = [INF] * (amount + 1)
best[0] = 0                                 # only zero is genuinely free
for a in range(1, amount + 1):
    for c in coins:
        if c <= a and best[a - c] + 1 < best[a]:
            best[a] = best[a - c] + 1
return -1 if best[amount] == INF else int(best[amount])
```

**Why it matters.** Using 0 as the "cannot be made" marker collides with the one amount that
genuinely costs zero coins. Worse, the value propagates: any amount reachable
from an unreachable one inherits the fiction and comes back with a small,
confident, wrong count.

The output is a non-negative integer in every case, so nothing looks amiss. A
vending machine built on it would report that it had dispensed change it does not
have.

An "impossible" sentinel must be a value the valid range can never take.
Infinity works, and the conversion to -1 happens once, at the boundary.

**Proved by:** `test_p03_coin_change_min`

## Defect 2 — Non-adjacent selection forces alternation

**Location:** `house_robber`, the transition

**The bug:**

```python
skip, take = take, skip + x     # `take` MUST include x - skipping is never an option
```

**The fix:**

```python
# At each element: either skip it (keep the previous best) or take it
# (previous-but-one best, plus x). max() is what allows a run of skips.
skip, take = take, max(take, skip + x)
```

**Why it matters.** Omitting the `max` removes the choice the problem is built on. The recurrence
becomes "take this element and add it to the total from two back", which forces a
strictly alternating selection.

On `[2, 1, 1, 2]` that yields `2 + 1 = 3`, because taking positions 0 and 3 —
which are not adjacent, and total 4 — requires skipping *two* in a row. The
answer is a valid selection's sum, just not the maximum, so it passes any check
that only verifies the adjacency constraint.

The general shape of a DP transition is a maximum over the available choices. If
there is no `max` or `min` in it, ask which choice went missing.

**Proved by:** `test_p02_house_robber`

## Defect 3 — Equal values extend the increasing subsequence

**Location:** `lis`, the inner comparison

**The bug:**

```python
if nums[j] <= nums[i]:      # <= counts equal values as an increase
```

**The fix:**

```python
if nums[j] < nums[i]:       # strictly increasing
```

**Why it matters.** `<=` admits equal values, so the function computes the longest *non-decreasing*
subsequence. On `[7, 7, 7, 7]` it reports 4, describing a subsequence that does
not increase at any step.

Every value returned is a real subsequence length, and on strictly-increasing
test data the two definitions coincide — so the bug only appears when the input
contains duplicates.

Strict versus non-strict is a specification decision that shows up as a single
character. Read the statement, then write the operator.

**Proved by:** `test_p04_lis`

## Defect 4 — A negative product should have become the maximum

**Location:** `max_product_subarray`, the single-variable state

**The bug:**

```python
cur = max(x, cur * x)       # tracks only the running MAXIMUM
best = max(best, cur)
```

**The fix:**

```python
# A negative multiplier turns the smallest product into the largest, so both
# extremes have to be carried. Compute both from the PREVIOUS pair.
candidates = (x, cur_max * x, cur_min * x)
cur_max = max(candidates)
cur_min = min(candidates)
best = max(best, cur_max)
```

**Why it matters.** For maximum *sum*, a single running best is enough. For maximum *product* it is
not: multiplying by a negative number flips the ordering, so the most negative
product so far is a candidate for the largest as soon as another negative
appears.

On `[-2, 3, -4]` the optimum is the whole array, `(-2) × 3 × (-4) = 24`, and it
is only reachable by having kept `-6` — a value a maximum-only state discards
immediately. The reported answer is a genuine subarray product, merely not the
best one.

Choosing the state is the first and most consequential step in any DP. When a
transition can reverse the ordering, one extreme is not enough state.

**Proved by:** `test_p07_max_product_subarray`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | An impossible amount is reported as costing zero coins | No |
| 2 | Non-adjacent selection forces alternation | No |
| 3 | Equal values extend the increasing subsequence | No |
| 4 | A negative product should have become the maximum | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
