# Debug Lab 13 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — Every subset comes back empty

**Location:** `subsets`, the recording of a result

**The bug:**

```python
def backtrack(start):
    out.append(path)        # stores a REFERENCE to the live, mutating list
```

**The fix:**

```python
def backtrack(start):
    out.append(path[:])     # a snapshot: path is mutated after this returns
```

**Why it matters.** `path` is one list object reused for the whole search. Appending it stores a
reference, so every entry in `out` is the *same* object — and by the time the
search finishes, every `append` has been undone by its matching `pop`, leaving
that shared object empty.

The result has exactly the right length, which is why a count-based check passes.
Its contents are 2ⁿ copies of the empty list.

This is the most common backtracking bug there is, and it generalises: whenever
you record mutable state that the algorithm will keep changing, record a copy.

**Proved by:** `test_p01_subsets`

## Defect 2 — Permutations are produced but the `used` flag is never cleared

**Location:** `permutations`, the undo after recursion

**The bug:**

```python
path.append(ordered[i])
backtrack()
path.pop()              # only ONE of the two pieces of state is undone
# used[i] is never reset
```

**The fix:**

```python
path.append(ordered[i])
backtrack()
path.pop()
used[i] = False         # both pieces of state must be restored
```

**Why it matters.** Backtracking is a contract: every change made on the way down must be undone on
the way back up. Here `path` is restored and `used` is not, so an element
consumed by the first branch stays permanently consumed for every sibling branch.

The search then finds only the permutations reachable before the flags run out —
one, in most cases. Each result it does produce is a genuine permutation, so
validity checks pass and only the *count* is wrong.

When a recursive step mutates several structures, undoing them is not optional
and not partial. Pair every mutation with its inverse, visibly adjacent.

**Proved by:** `test_p02_permutations`

## Defect 3 — Candidates cannot be reused

**Location:** `combination_sum`, the recursive call's start index

**The bug:**

```python
backtrack(i + 1, remaining - ordered[i])    # i + 1 forbids reusing candidate i
```

**The fix:**

```python
# `i`, not `i + 1`: the same candidate may be chosen again. Never going
# backwards is what still keeps each combination unique.
backtrack(i, remaining - ordered[i])
```

**Why it matters.** Passing `i + 1` advances past the current candidate, which is exactly right for a
*subset* problem where each element may be used once — and exactly wrong here,
where reuse is permitted.

Every combination returned is valid and sums to the target; the set is simply
incomplete. `[2]` with target 6 returns nothing at all, and `[2,3,6,7]` with
target 7 loses `[2,2,3]`.

The distinction between `i` and `i + 1` in a backtracking loop is precisely the
distinction between with-replacement and without-replacement. Decide which the
problem wants before writing the call.

**Proved by:** `test_p04_combination_sum`

## Defect 4 — N-Queens finds too many solutions

**Location:** `n_queens`, the placement guard and its bookkeeping

**The bug:**

```python
cols, diag = set(), set()       # only ONE diagonal direction is tracked
...
if col in cols or (row - col) in diag:
    continue
```

**The fix:**

```python
cols, diag, anti = set(), set(), set()
...
# A queen attacks along BOTH diagonals: row - col is constant on one,
# row + col on the other.
if col in cols or (row - col) in diag or (row + col) in anti:
    continue
cols.add(col)
diag.add(row - col)
anti.add(row + col)
place(row + 1)
cols.remove(col)
diag.remove(row - col)
anti.remove(row + col)
```

**Why it matters.** A queen attacks along two diagonals, and only one of them is being tracked.
Placements that share an anti-diagonal — `(0, 1)` and `(1, 0)`, for instance —
are accepted, so the search counts arrangements that are not solutions.

Every count comes back too high: 6 for n=4 where the answer is 2, and the
supposedly impossible n=2 and n=3 boards report solutions. The numbers are small
positive integers of exactly the expected shape, and n=1 is still correct.

Constraint problems fail quietly when a constraint is simply absent. Enumerate
the attack directions on paper first, then check that each one appears in the
guard.

**Proved by:** `test_p07_n_queens`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | Every subset comes back empty | No |
| 2 | Permutations are produced but the `used` flag is never cleared | No |
| 3 | Candidates cannot be reused | No |
| 4 | N-Queens finds too many solutions | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
