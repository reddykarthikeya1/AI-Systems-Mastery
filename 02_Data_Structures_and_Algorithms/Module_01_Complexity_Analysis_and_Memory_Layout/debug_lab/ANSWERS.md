# Debug Lab 01 — Answers

> Read this only after you have written a diagnosis for each symptom.

5 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — A noisy measurement flips the growth classification

**Location:** `classify_growth`, the ratio computation

**The bug:**

```python
first_size, first_time = timings[0]
last_size, last_time = timings[-1]
ratio = last_time / first_time      # spans ALL the doublings, not one
```

**The fix:**

```python
ratios = [
    t_next / t_prev
    for (_, t_prev), (_, t_next) in zip(timings, timings[1:])
    if t_prev > 0
]
ratio = sum(ratios) / len(ratios)   # mean per-doubling ratio
```

**Why it matters.** The function compares the first and last timings, so the ratio compounds across
every doubling instead of measuring one. Over three doublings a linear algorithm
reaches 4.0 and a quadratic one reaches 16.0 — but the thresholds were written
for a *single* doubling, where the values are 2 and 4. Every linear algorithm
measured over more than two samples is therefore reported as quadratic, and the
capacity plan buys hardware for a cost curve that does not exist.

Averaging the consecutive ratios both fixes the scale and makes one noisy sample
harmless, which is the second half of the requirement.

**Proved by:** `test_p01_classify_growth`

## Defect 2 — The amortised-copy calculation cannot finish at scale

**Location:** `total_copies_for_appends`, the `while` loop body

**The bug:**

```python
while size < n:
    if size == capacity:
        copies += capacity
        capacity *= 2
    size += 1                   # one iteration PER ELEMENT
```

**The fix:**

```python
while size < n:
    if size == capacity:
        copies += capacity
        capacity *= 2
    # Fill the remaining capacity in one step: only ~log2(n) iterations total.
    take = min(capacity - size, n - size)
    size += take
```

**Why it matters.** The answer is correct; the method is O(n) when it should be O(log n). At the
sizes in this report it merely feels slow, and at the documented upper bound of
10**9 it does not return at all.

This is the most easily missed class of defect, because the *output* is right.
Nothing in a correctness test catches it — only a test that asserts the
complexity by running at a scale the wrong implementation cannot survive, which
is exactly what the problem-bank test does.

**Proved by:** `test_p02_amortized_copies`

## Defect 3 — Binary search comparisons are wrong at large n

**Location:** `max_binary_search_comparisons`, the `math.log2` call

**The bug:**

```python
return int(math.log2(n)) + 1        # float rounding at large n
```

**The fix:**

```python
# bit_length() is floor(log2(n)) + 1 exactly, with no float involved.
return n.bit_length()
```

**Why it matters.** `math.log2` works in double precision, which has 53 bits of mantissa.
Above 2**53 the input cannot be represented exactly, so the logarithm is
computed from a rounded value and `int()` truncates the result — sometimes one
lower than the truth. At 10**18 the answer comes out one comparison short.

Being one comparison short does not sound serious until you remember what the
number is for: sizing a fixed-depth search structure. One level short means the
deepest keys are unreachable, and the failure appears only for the rarest inputs.

The general lesson: when an integer answer is required, compute it with integers.
`bit_length()` is exact at every magnitude.

**Proved by:** `test_p03_binary_search_steps`

## Defect 4 — A comparison count comes back as a float

**Location:** `count_pair_iterations`, the division

**The bug:**

```python
return n * (n - 1) / 2          # true division -> float
```

**The fix:**

```python
return n * (n - 1) // 2         # floor division -> exact int
```

**Why it matters.** `/` is true division and always produces a float, even when both operands are
integers and the result is mathematically whole. `n * (n - 1)` is always even, so
the value is an integer — but above 2**53 a float cannot represent it, and the
printed count is silently wrong in its low digits.

At n = 10**9 the exact answer is 499999999500000000 and the float is
499999999500000000.0 — which looks identical until it is compared for equality,
used as a dict key, or fed to something that expects an int.

`//` keeps the whole computation in Python's arbitrary-precision integers, where
it is exact at any size.

**Proved by:** `test_p04_pair_iterations`

## Defect 5 — An unsupported complexity class is silently reported as 'does not fit'

**Location:** `fits_budget`, the final `else` branch

**The bug:**

```python
else:
    return False        # unknown class silently means 'does not fit'
```

**The fix:**

```python
else:
    raise ValueError(f"unsupported complexity class: {complexity!r}")
```

**Why it matters.** Returning `False` for an unrecognised class conflates two completely different
statements: *this algorithm is too slow* and *I do not know what you asked me*.

The consequence is worse than a missing feature. A typo in a complexity string
produces a confident "does not fit", so a perfectly viable design is rejected on
the strength of a spelling mistake — and because `False` is a plausible answer,
nobody investigates.

A function that cannot answer must say so. `O(n!)` at n=10 genuinely fits, and
`O(n^4)` is a question the function has no opinion about; both deserve something
other than a quiet `False`.

**Proved by:** `test_p05_fits_budget`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | A noisy measurement flips the growth classification | No |
| 2 | The amortised-copy calculation cannot finish at scale | No |
| 3 | Binary search comparisons are wrong at large n | No |
| 4 | A comparison count comes back as a float | No |
| 5 | An unsupported complexity class is silently reported as 'does not fit' | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
