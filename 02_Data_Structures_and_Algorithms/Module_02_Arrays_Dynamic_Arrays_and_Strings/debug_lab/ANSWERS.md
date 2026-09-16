# Debug Lab 02 — Answers

> Read this only after you have written a diagnosis for each symptom.

5 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — An element pairs with itself

**Location:** `two_sum`, the order of the insert and the lookup

**The bug:**

```python
for i, x in enumerate(nums):
    seen[x] = i                     # inserted FIRST
    complement = target - x
    if complement in seen:          # so x can match itself
        return [seen[complement], i]
```

**The fix:**

```python
for i, x in enumerate(nums):
    complement = target - x
    if complement in seen:          # check against EARLIER elements only
        return [seen[complement], i]
    seen[x] = i
```

**Why it matters.** Inserting before looking up means the current element is already in the map when
its own complement is sought. Whenever `2 * x == target`, `x` matches itself and
the function returns the same index twice.

The output is structurally valid — two indices, and their values do sum to the
target — so a caller that only checks the sum sees nothing wrong. It is the
*distinctness* requirement that is violated, and nothing about the return value
advertises that.

Checking before inserting means the map only ever holds strictly earlier
elements, which is the invariant the problem actually requires.

**Proved by:** `test_p01_two_sum`

## Defect 2 — An all-negative window sums to zero

**Location:** `max_window_sum`, the initialisation of `best`

**The bug:**

```python
best = 0                        # 0 is not a candidate answer
total = sum(nums[:k])
best = max(best, total)
```

**The fix:**

```python
total = sum(nums[:k])
best = total                    # the first real window IS the starting best
```

**Why it matters.** Initialising an extremum to zero smuggles in a candidate that does not exist in
the data. When every window is negative, `max` keeps the fabricated 0 and the
function reports a window sum that no window has.

This bug is invisible on any input containing a positive window, which is most
test data — so it passes review, ships, and then produces a wrong number the
first time a metric goes negative. Seeding the extremum from the first real
element removes the possibility entirely, and is the habit worth forming.

**Proved by:** `test_p02_max_window_sum`

## Defect 3 — Subarrays starting at index 0 are not counted

**Location:** `subarray_sum_k`, the initialisation of `counts`

**The bug:**

```python
counts: dict[int, int] = {}     # the empty prefix is missing
```

**The fix:**

```python
# {0: 1} represents the empty prefix, which is what makes a subarray
# starting at index 0 countable.
counts: dict[int, int] = {0: 1}
```

**Why it matters.** The method counts pairs of prefix sums differing by `k`. A subarray starting at
index 0 pairs with the *empty* prefix, whose sum is 0 — so unless the map is
seeded with `{0: 1}`, every such subarray is missed.

The undercount is small and data-dependent: it appears only when a qualifying
subarray happens to start at the first element. On most inputs the answer is
merely a little low, which is the hardest kind of wrong to notice, and the
reason this problem's tests include an explicit assertion for that case.

**Proved by:** `test_p04_subarray_sum_k`

## Defect 4 — Every reported substring length is far too short

**Location:** `longest_k_distinct`, the shrink loop's comparison

**The bug:**

```python
while len(counts) >= k:         # >= shrinks one character too eagerly
    leaving = s[left]
    counts[leaving] -= 1
    if counts[leaving] == 0:
        del counts[leaving]
    left += 1
```

**The fix:**

```python
while len(counts) > k:          # k distinct is ALLOWED, k+1 is not
    leaving = s[left]
    counts[leaving] -= 1
    if counts[leaving] == 0:
        del counts[leaving]
    left += 1
```

**Why it matters.** `>=` shrinks the window as soon as it holds `k` distinct characters, but `k`
distinct is exactly what the problem permits. The window is therefore capped at
`k - 1` distinct characters and every answer comes back short — for k=2 it
reports 1 where the truth is 3.

The output is a plausible small integer and nothing raises, so the only way to
catch it is to compare against a known-correct value. That is why this problem's
tests carry both hand-computed expectations and a brute-force cross-check.

The wider habit: when a bound says "at most k", write the loop condition by
asking *which state is illegal* — here `k + 1` — rather than by pattern-matching
a comparison operator.

**Proved by:** `test_p03_longest_k_distinct`

## Defect 5 — The ship capacity search starts below the largest package

**Location:** `min_ship_capacity`, the lower bound of the binary search

**The bug:**

```python
lo, hi = 1, sum(weights)        # 1 cannot carry a heavy package
```

**The fix:**

```python
# A single package must fit on its own, so that is the true lower bound.
lo, hi = max(weights), sum(weights)
```

**Why it matters.** The search range admits capacities too small to carry the heaviest package.
`days_needed` does not reject those: for an oversized package it opens a new day
and then loads it anyway, so the count it returns is achievable only by a ship
that cannot actually exist.

Because the feasibility predicate lies for capacities below `max(weights)`,
binary search converges on one of them and returns a capacity that is impossible
to operate. Every number involved looks reasonable, and the plan is unbuildable.

The wider lesson for binary-search-on-the-answer: the bounds are part of the
correctness argument, not a formality. If the predicate is only meaningful on
part of the range, the range must be narrowed to where it is meaningful.

**Proved by:** `test_p06_min_ship_capacity`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | An element pairs with itself | No |
| 2 | An all-negative window sums to zero | No |
| 3 | Subarrays starting at index 0 are not counted | No |
| 4 | Every reported substring length is far too short | No |
| 5 | The ship capacity search starts below the largest package | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
