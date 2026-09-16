# Debug Lab 12 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — Merging a nested block shrinks the merged range

**Location:** `merge_intervals`, the merge assignment

**The bug:**

```python
if start <= last_end:
    out[-1] = (last_start, end)      # blindly adopts the incoming end
```

**The fix:**

```python
if start <= last_end:
    # A nested interval must not shrink the accumulated range.
    out[-1] = (last_start, max(last_end, end))
```

**Why it matters.** Sorting by start guarantees the incoming interval begins no earlier, but says
nothing about where it *ends*. A fully nested block ends sooner, and adopting its
end truncates the merged range.

`[(1, 10), (2, 3)]` becomes `(1, 3)`, silently discarding seven units of busy
time. The output is still a sorted list of disjoint intervals, so any structural
check passes — a calendar built on it would show free time that is not free.

Sorting establishes one ordering, not two. Whenever a merge combines two values,
ask explicitly which one wins.

**Proved by:** `test_p02_merge_intervals`

## Defect 2 — Fewer meetings are scheduled than could fit

**Location:** `max_non_overlapping`, the sort key

**The bug:**

```python
for start, end in sorted(intervals):     # sorted by START
```

**The fix:**

```python
# Sort by END: the earliest-finishing meeting leaves the most room for
# everything after it. That is the exchange argument in one line.
for start, end in sorted(intervals, key=lambda iv: iv[1]):
```

**Why it matters.** Merging and scheduling are different questions and need different orderings.
Merging cares where intervals *begin*; scheduling cares where they *end*, because
the meeting that finishes earliest leaves the most room for the rest.

Sorting by start makes the algorithm greedily take `(1, 10)` and then fit only
one more, reporting 2 where 3 is achievable. The answer is a genuine
non-overlapping selection, merely not the largest — so it satisfies every
validity check you could write about the output alone.

This is the highest-value fact in the module, and it is worth memorising in those
words: **sort by start to merge, sort by end to schedule.**

**Proved by:** `test_p03_max_non_overlapping`

## Defect 3 — A trade can buy and sell on the same day

**Location:** `max_profit_stock`, the order of the two updates

**The bug:**

```python
if price < cheapest:
    cheapest = price            # updated FIRST
if price - cheapest > best:     # ...so today can be sold against itself
    best = int(price - cheapest)
```

**The fix:**

```python
# Evaluate the sale against the minimum from a STRICTLY EARLIER day, then
# fold today's price in.
if price - cheapest > best:
    best = int(price - cheapest)
if price < cheapest:
    cheapest = price
```

**Why it matters.** Updating the running minimum before computing the profit lets a day be both the
purchase and the sale. The profit is then `price - price == 0`, which is
harmless — until you notice it means the invariant "buy strictly before sell" is
not being enforced at all.

Here the damage is bounded because a same-day trade yields exactly 0 and `best`
starts at 0. Change the problem slightly — allow short selling, or seed `best`
from the data rather than 0 — and the same ordering bug produces a confidently
wrong positive number.

Statement order inside a loop body is part of the algorithm. When a running
aggregate and a comparison against it share an iteration, decide deliberately
which comes first.

**Proved by:** `test_p01_max_profit_stock`

## Defect 4 — An impossible circuit reports a starting station

**Location:** `gas_station`, the missing feasibility check

**The bug:**

```python
start = 0
tank = 0
for i, (g, c) in enumerate(zip(gas, cost)):
    ...
return start            # always an index, even when no circuit is possible
```

**The fix:**

```python
# If total gas is less than total cost, no starting point can work.
if sum(gas) < sum(cost):
    return -1

start = 0
tank = 0
for i, (g, c) in enumerate(zip(gas, cost)):
    ...
return start
```

**Why it matters.** The single-pass scan is correct *given* that a solution exists — that is the
precondition the whole argument rests on. Without the global feasibility check,
the loop still terminates and still returns an index, which is a plausible answer
to a question that has none.

`gas=[2,3,4]`, `cost=[3,4,3]` has 9 units of fuel and 10 units of demand, so no
lap is possible from anywhere. The function returns 3 — not even a valid station
index for a 3-element list.

Greedy algorithms very often carry a precondition like this. When the argument
begins "assuming a solution exists", that assumption is a check you owe the
caller.

**Proved by:** `test_p07_gas_station`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | Merging a nested block shrinks the merged range | No |
| 2 | Fewer meetings are scheduled than could fit | No |
| 3 | A trade can buy and sell on the same day | No |
| 4 | An impossible circuit reports a starting station | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
