# Debug Lab 05 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — Non-anagrams are grouped together

**Location:** `group_anagrams`, the choice of canonical key

**The bug:**

```python
key = frozenset(word)       # discards how many times each letter appears
```

**The fix:**

```python
# A sorted-letter string (or a 26-slot count tuple) preserves multiplicity.
key = "".join(sorted(word))
```

**Why it matters.** A set records *which* letters appear and throws away *how many times*. `"aab"`
and `"abb"` both reduce to `{'a', 'b'}`, so they land in the same bucket despite
not being anagrams.

Every group is non-empty and every word appears exactly once, so the output
passes any structural check. It is only wrong about the thing it claims to
compute, and only for words whose letter multiplicities differ — which most
short test cases avoid.

The lesson generalises past anagrams: a canonical form is only valid if two
inputs share it *exactly when* they are equivalent. Losing information makes the
key too coarse, and a hash map cannot tell you that.

**Proved by:** `test_p01_group_anagrams`

## Defect 2 — Frequency ties come out in an unpredictable order

**Location:** `top_k_frequent`, the sort key

**The bug:**

```python
ordered = sorted(counts.items(), key=lambda kv: -kv[1])     # ties unresolved
```

**The fix:**

```python
# Ascending value breaks frequency ties, so the result is deterministic.
ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
```

**Why it matters.** Python's sort is stable, so items with equal counts keep the order they had in
`counts.items()` — which is dict insertion order, i.e. the order the values first
appeared in the input. The function's output therefore depends on input ordering
in a way the specification does not mention.

That is not a crash and often not even wrong; it is *unspecified*. The result is
a test that passes on one input ordering and fails on a permutation of the same
data, which is among the most confusing kinds of failure to debug.

Any function whose contract says "the top k" must define what happens on a tie,
and then implement that definition in the sort key.

**Proved by:** `test_p02_top_k_frequent`

## Defect 3 — The consecutive-run scan is quadratic

**Location:** `longest_consecutive`, the missing run-start guard

**The bug:**

```python
for x in present:
    length = 1              # every member of a run starts its own walk
    cur = x
```

**The fix:**

```python
for x in present:
    # Only walk from a genuine run start, so each run is traversed exactly once.
    if x - 1 in present:
        continue
    length = 1
    cur = x
```

**Why it matters.** Every element begins a walk, so a run of length L is traversed L times — once
from each of its members. On a single long run that is O(n²): 20,000 elements
means 200 million membership tests.

The answers are all correct, which is what makes this dangerous. Correctness
tests pass, review passes, and the function is quietly quadratic until the input
grows. The stated constraint is 10⁵ elements, where the wrong version does 5
billion operations.

The guard is one line and it changes the complexity class. Any nested walk inside
a loop deserves the question: *how many times is the same element visited?*

**Proved by:** `test_p03_longest_consecutive`

## Defect 4 — The distance limit is ignored entirely

**Location:** `contains_nearby_duplicate`, the missing eviction

**The bug:**

```python
window.add(x)
# nothing ever leaves the set, so `window` is really 'everything seen'
return False
```

**The fix:**

```python
window.add(x)
if len(window) > k:
    window.remove(nums[i - k])      # the element that just left the window
return False
```

**Why it matters.** The parameter `k` is accepted and never used. The set accumulates every element
ever seen, so the function answers a different question — *is there any
duplicate at all?* — and reports True for duplicates arbitrarily far apart.

`[1, 2, 3, 1]` with k=2 comes back True when the two 1s are three apart. The
answer is a plausible boolean, and it is right whenever the duplicates happen to
be close, so roughly half of any test set passes.

An unused parameter is a strong signal. If a constraint appears in the signature
and nowhere in the body, the function is not solving the stated problem.

**Proved by:** `test_p05_contains_nearby_duplicate`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | Non-anagrams are grouped together | No |
| 2 | Frequency ties come out in an unpredictable order | No |
| 3 | The consecutive-run scan is quadratic | No |
| 4 | The distance limit is ignored entirely | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
