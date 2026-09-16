# Debug Lab 07 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — K-th largest returns the k-th smallest

**Location:** `kth_largest`, the negation

**The bug:**

```python
heapq.heappush(heap, -x)    # negated => a MAX-heap
if len(heap) > k:
    heapq.heappop(heap)     # ...so this evicts the LARGEST, keeping the smallest k
return -heap[0]
```

**The fix:**

```python
# A MIN-heap of size k: the root is the weakest of the best k, which is
# exactly what should be evicted.
heapq.heappush(heap, x)
if len(heap) > k:
    heapq.heappop(heap)
return heap[0]
```

**Why it matters.** Negating the values turns `heapq` into a max-heap, so `heappop` removes the
largest element — and the survivors are the k *smallest*. The function computes
the k-th smallest and calls it the k-th largest.

For k=1 and for all-equal inputs the two answers coincide, which is exactly the
kind of coincidence that gets a wrong implementation shipped.

The rule is worth memorising because it is counter-intuitive: to keep the k
**largest**, use a **min**-heap of size k, so the root is the weakest member of
the set you are keeping and is the right one to throw away.

**Proved by:** `test_p01_kth_largest`

## Defect 2 — The merge stops as soon as any one list is exhausted

**Location:** `merge_k_sorted`, the `else` branch

**The bug:**

```python
if nxt < len(lists[li]):
    heapq.heappush(heap, (lists[li][nxt], li, nxt))
else:
    break                   # one list ending stops the whole merge
```

**The fix:**

```python
if nxt < len(lists[li]):
    heapq.heappush(heap, (lists[li][nxt], li, nxt))
# No else: the outer `while heap` already stops when everything is consumed.
```

**Why it matters.** Exhausting one input list is a completely ordinary event — it happens k times in
any successful merge. Treating it as a termination condition ends the merge at
the first one, discarding everything still queued in the other lists.

The output is correctly sorted and non-empty, so a sortedness check passes.
Only the *count* is wrong, and how wrong depends on which list runs out first —
so the loss varies with the data and is easy to dismiss as a fluke.

The loop already has the right termination condition: `while heap`. When every
list is drained the heap empties on its own.

**Proved by:** `test_p02_merge_k_sorted`

## Defect 3 — The median is wrong for every even-length prefix

**Location:** `streaming_median`, the branch that selects the median formula

**The bug:**

```python
if len(lower) >= len(upper):    # equal sizes means an EVEN count
    out.append(float(-lower[0]))    # ...so this takes only the lower value
else:
    out.append((-lower[0] + upper[0]) / 2.0)
```

**The fix:**

```python
if len(lower) > len(upper):     # strictly greater means an ODD count
    out.append(float(-lower[0]))
else:                           # equal sizes: average the two middles
    out.append((-lower[0] + upper[0]) / 2.0)
```

**Why it matters.** After rebalancing, `len(lower) == len(upper)` means an even number of values, and
the median is the average of the two roots. `>=` sends that case down the
odd-count branch, which returns the lower of the two middle values instead of
their mean.

Every odd-length prefix is still correct, so half the output is right and the
errors are small — for `[1, 2]` it reports 1.0 instead of 1.5. A drift of half a
unit in a monitoring median is exactly the kind of discrepancy that gets
attributed to sampling rather than to a bug.

The comparison operator is where the parity decision lives. Write down which
size relation corresponds to which parity before choosing between `>` and `>=`.

**Proved by:** `test_p03_streaming_median`

## Defect 4 — Meeting rooms depends on the order of the input

**Location:** `min_meeting_rooms`, the missing sort

**The bug:**

```python
for start, end in intervals:            # unsorted
    if ends and ends[0] <= start:
        heapq.heappop(ends)
```

**The fix:**

```python
# Earliest start first: the reuse test is only meaningful in start order.
for start, end in sorted(intervals):
    if ends and ends[0] <= start:
        heapq.heappop(ends)
```

**Why it matters.** The reuse test asks whether some room has already been vacated by the time this
meeting starts. That question only makes sense if meetings are considered in
chronological order — otherwise a later meeting can free a room for an earlier
one, which is not how time works.

Without the sort the answer becomes a function of input ordering: the same three
meetings give different room counts depending on how they were listed. Both
numbers are plausible, and neither is reliably correct.

A result that changes when you shuffle the input is the clearest possible signal
of a missing ordering assumption. It is also the cheapest property to test.

**Proved by:** `test_p06_min_meeting_rooms`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | K-th largest returns the k-th smallest | No |
| 2 | The merge stops as soon as any one list is exhausted | No |
| 3 | The median is wrong for every even-length prefix | No |
| 4 | Meeting rooms depends on the order of the input | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
