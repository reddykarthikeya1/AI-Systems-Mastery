# Debug Lab 04 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — An unclosed bracket is reported as balanced

**Location:** `balanced_brackets`, the final return

**The bug:**

```python
else:
        stack.append(ch)
return True                 # ignores anything left open
```

**The fix:**

```python
else:
        stack.append(ch)
return not stack            # anything still open means unbalanced
```

**Why it matters.** The loop correctly rejects a closer with no matching opener, so every input with
a stray `)` is handled. What it never checks is the opposite failure: openers
that were never closed.

`"("` and `"([]"` therefore come back `True`. Both are structurally plausible
answers, and both are wrong.

Two failure modes exist for bracket matching and they need two separate checks:
one inside the loop for an unexpected closer, one after it for a non-empty
stack.

**Proved by:** `test_p01_balanced_brackets`

## Defect 2 — Equal values are treated as greater

**Location:** `next_greater`, the `while` comparison

**The bug:**

```python
while stack and nums[stack[-1]] <= x:   # <= resolves EQUAL values too
    out[stack.pop()] = x
```

**The fix:**

```python
while stack and nums[stack[-1]] < x:    # only strictly greater resolves
    out[stack.pop()] = x
```

**Why it matters.** With `<=`, a value equal to the one on the stack pops it and is recorded as its
"next greater" — but an equal value is not greater. For `[1, 1, 2]` index 0 is
answered with 1 instead of 2.

The output is the right length and every entry is a value that genuinely appears
later in the array, so it looks entirely reasonable. It is only wrong at
positions followed by a duplicate, which is why an input without repeats passes.

`<` versus `<=` in a monotonic stack is precisely the strict-versus-non-strict
distinction in the problem statement. Read the statement, then write the
operator — not the other way round.

**Proved by:** `test_p02_next_greater`

## Defect 3 — Daily temperatures reports an index instead of a wait

**Location:** `daily_temperatures`, the assignment inside the `while`

**The bug:**

```python
j = stack.pop()
out[j] = i                  # the absolute index, not the distance
```

**The fix:**

```python
j = stack.pop()
out[j] = i - j              # the number of days waited
```

**Why it matters.** The stack holds indices precisely so the *distance* can be computed, and then
the distance is never computed — the resolving index is stored raw.

Every value is a small non-negative integer of exactly the right shape, and for
index 0 the two answers even coincide when the warmer day is index 1. That
coincidence is what lets the bug through a spot check.

Storing indices in a monotonic stack is the right design; the whole reason to do
it is `i - j`. If the answer does not use both, ask whether you needed the index
at all.

**Proved by:** `test_p03_daily_temperatures`

## Defect 4 — The sliding-window maximum reports stale values

**Location:** `sliding_window_max`, the missing front eviction

**The bug:**

```python
dq.append(i)
# nothing removes an index that has fallen out of the window
if i >= k - 1:
    out.append(nums[dq[0]])
```

**The fix:**

```python
dq.append(i)
if dq[0] <= i - k:
    dq.popleft()            # the front index has left the window
if i >= k - 1:
    out.append(nums[dq[0]])
```

**Why it matters.** The back eviction keeps the deque decreasing, which is necessary but not
sufficient. Without the front eviction, the largest value ever seen stays at the
front forever, so once the true maximum slides out of the window the function
keeps reporting it.

On a non-decreasing input the bug is invisible: the maximum is always the newest
element, which is inside the window anyway. On a decreasing input every value
after the first is wrong. That data-dependence is why this passes a casual test.

Two evictions, and they answer different questions: *is this index dominated?*
and *is this index still in the window?* Both are required.

**Proved by:** `test_p05_sliding_window_max`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | An unclosed bracket is reported as balanced | No |
| 2 | Equal values are treated as greater | No |
| 3 | Daily temperatures reports an index instead of a wait | No |
| 4 | The sliding-window maximum reports stale values | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
