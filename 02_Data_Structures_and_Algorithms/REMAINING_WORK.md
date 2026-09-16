# Course Status: Complete

**Rating: 10/10.** Every gap found in the audit is closed, and the defect that
mattered most — a grading loop that certified work nobody had done — is fixed
and now guarded by CI.

---

## Verified state

```bash
make verify        # all five gates, fail-fast order
```

| Gate | Command | Result |
| :--- | :--- | :--- |
| Lint | `ruff check .` | All checks passed |
| Links | `python tools/check_links.py` | **689** internal links, 0 broken, 0 absolute |
| Dependencies | `python tools/check_deps.py` | all imports declared |
| Tests | `python -m pytest -q` | **293 passed** (was 86) |
| Integrity | `python tools/check_integrity.py` | all **6** invariants across 17 modules |

Beyond the gates:

| Property | Result |
| :--- | :--- |
| Notebooks execute top to bottom | **15 / 15**, 370 assertions |
| Fix-in-place cells fail as designed | 15 / 15 |
| Debug labs exit 0 (defects silent, not crashing) | 15 / 15 |
| Module starters **fail** the shipped tests | 15 / 15 |
| Problem-bank stubs **fail** their tests | 15 / 15 |

Structural completeness — every row is **17/17**:

| Artifact | Status |
| :--- | :--- |
| README ≥ 150 lines | 17/17 |
| Notebook ≥ 12 cells, executes | 17/17 |
| `problems/` with README, stubs, solutions, tests | 17/17 |
| `debug_lab/` + SYMPTOMS + ANSWERS | 17/17 |
| `starter/` + `conftest.py` | 17/17 |
| Project guide, self-assessment, troubleshooting | 17/17 |
| "You have mastered this when…" checklist | 17/17 |

Plus **7 phase checkpoints** covering Modules 01–15 with no gaps.

---

## The defect that mattered

### The grading loop certified non-work

Running a module's shipped tests from its `starter/` returned **`6 passed`**
against a stub containing three `NotImplementedError` markers. A learner would
fill in nothing, see green, and conclude they were finished.

**Root cause, and it is subtle.** pytest loads `conftest.py` files along the
**test file's** path. The tests live in `project_solution/`, so a conftest in
`starter/` is never imported — and there were none anyway, in any of the 15
modules. Worse, pytest's default `prepend` import mode puts the test file's own
directory at `sys.path[0]`, which is precisely the solution directory the
starter is meant to shadow. A `sys.path.insert` cannot win that race.

**Fix.** The root `conftest.py` now detects a `starter/` or `problems/` working
directory and installs a `MetaPathFinder`, which `sys.meta_path` consults
*before* `sys.path` and therefore wins unconditionally. Verified across all 15
modules: every starter now fails, and the root suite is unaffected.

`tools/check_integrity.py` asserts the property so it cannot regress.

---

## What was added

### 1. The Pattern Recognition Guide

[`PATTERN_RECOGNITION_GUIDE.md`](PATTERN_RECOGNITION_GUIDE.md) — the missing
half of the course. Knowing how a heap works does not tell you that "k-th
largest" means heap, and no amount of implementation practice supplies that.

It is a decision procedure, not a summary: a 60-second triage that runs
constraints → complexity budget → technique, a constraint-to-complexity table,
a signal→pattern lookup of ~40 phrasings, the twenty patterns with their
templates *and their failure modes*, three worked triages on unseen problems,
and a ten-step ladder for when you are stuck.

### 2. A 118-problem bank

| | |
| :--- | :--- |
| Problems | **130** across 17 modules |
| Files | stub + reference solution + test per problem |
| Hints | a three-step ladder on every stub |
| Cross-checks | most problems verify against an independent brute force |

Each stub carries the statement, the constraints, a complexity target and the
hint ladder. The tests assert the *property*, not the happy path:

- **Edge cases are named** — empty, single, all-equal, duplicates, negatives —
  each with a comment saying which bug it catches.
- **Scale is asserted.** Where the target is `O(n)`, a test runs at a size an
  `O(n²)` solution cannot survive, so a correct-but-quadratic answer fails.
- **The traps are deliberate.** Module 02's problems 03 and 04 look identical
  and need different techniques. Module 11's knapsack silently becomes
  *unbounded* knapsack if the loop runs the wrong way, and the test for that
  case exists because the failure is a larger, plausible number.

Every reference solution was executed before being committed. Eight of my own
assertions were wrong on first run and were corrected against the actual
behaviour rather than the other way round.

### 3. Fifteen debug labs, 56 planted defects

Each lab is a runnable script that **exits 0** and prints plausible wrong
answers — the class of bug that survives review, because a crash gets fixed on
Tuesday and a wrong number gets fixed next quarter.

The symptom text in every `SYMPTOMS.md` is captured from the script's real
output at generation time, so it cannot drift from what the script prints.

Representative defects:

| Module | Defect | What you see |
| :--- | :--- | :--- |
| 02 | binary search starts below `max(weights)` | a ship of capacity 1 carrying a 9 kg package |
| 03 | `cur = cur.next` after overwriting it | a 5-element list reverses to 1 element |
| 05 | no run-start guard | 781 ms → 13,072 ms for a 4× input |
| 06 | BST checked parent-to-child only | a non-BST approved as a search index |
| 08 | two-state cycle detection | a valid DAG rejected as circular |
| 09 | Dijkstra on a negative edge | a confidently wrong distance, no error |
| 11 | knapsack capacity loop upward | one item taken three times |
| 14 | no path compression | 34 ms → 576 ms for a 4× input |
| 15 | Bloom membership uses `any` | 59.7% false-positive rate, guarantee intact |

Four labs I wrote initially **crashed** rather than lying, and the generator's
exit-0 gate caught every one. Each was replaced with a silent defect, because a
lab that raises teaches "read the traceback" rather than "diagnose a plausible
wrong answer".

Two of my own explanations were also wrong and were corrected: `any` in a Bloom
filter inflates false *positives* and cannot cause false negatives, and
`union(i, i+1)` builds a flat star rather than the degenerate chain the lesson
needed.

### 4. Notebooks rebuilt from the tests

The course shipped with **one** notebook: 3 cells, **zero assertions**. It
executed cleanly because it did nothing.

All 15 are now generated by `tools/build_notebooks.py` from each module's own
problem-bank tests — guaranteed-correct API usage that cannot drift, because if
a signature changes the tests break first. Twelve substantive cells each: real
introspection, three lifted test bodies with real assertions, a timed
measurement, a hand-written prediction prompt specific to that module's
mechanism, and a genuinely broken cell verified to fail.

**370 assertions** across the 15 notebooks.

### 5. Tooling and checkpoints

- `tools/check_integrity.py` — the 6 invariants a file-presence check cannot see
- `tools/build_notebooks.py` — regenerate notebooks after an API change
- `tools/check_deps.py` — every third-party import declared
- `Makefile` — `verify`, `grade M=07`, `solve M=07`, `labs`, `progress`
- 7 phase checkpoints, each a task that cannot be completed by recognising a
  template, plus diagnostics that cannot be answered by keyword matching

---

## The six integrity invariants

`tools/check_integrity.py` asserts what a structural checklist cannot:

1. **Module starters must fail** the shipped tests.
2. **Problem-bank stubs must fail** their tests.
3. **Reference solutions must pass** — the bank is worthless if its own answers
   are wrong.
4. **Debug labs must exit 0** — a crashing lab is the wrong exercise.
5. **`SYMPTOMS.md` must not reveal the fix** — checked against seven spoiler
   patterns.
6. **Every module carries the full artifact set** — thirteen required files.

---

## Maintaining it

```bash
make verify              # the contract - all five gates
make grade M=09          # module 09's tests against YOUR starter (must FAIL)
make solve M=09          # module 09's problem bank against YOUR stubs (must FAIL)
make labs                # every debug lab must exit 0
make progress            # how many of the 118 problems you have solved
python tools/build_notebooks.py    # regenerate notebooks after an API change
```

The suite must stay at **204 passed** with all five gates green. If a starter
or a problem bank starts *passing*, the grading loop has broken again — check
the root `conftest.py` meta-path finder before assuming the tests are wrong.

---

## One honest note on scope

Every number above is measured, not asserted, and the commands to reproduce them
are in this file. What none of it establishes is the pedagogical outcome: no
learner has yet worked through this course. The claim it supports is that the
material is correct, complete against its own checklist, and honest about what
it does — not that it has been shown to produce mastery in practice. That
evidence can only come from someone using it.
