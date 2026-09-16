# Phase 2 Checkpoint Exam: Deep OOP & Robust Software Design

> **Phase Scope:** Modules 04–08 (OOP, Decorators & Context Managers, Errors, Serialization, Testing)  
> **Allocated Time:** 100 Minutes  
> **Format:** Closed-solution, architecture & testing build challenge.

---

## 🎯 The Exam Mission: Resilient Multi-Format Audit Ledger

Design a robust, tamper-evident transactional audit ledger engine. The engine must accept financial and administrative events, validate them through custom descriptor constraints, serialize to atomic JSON/CSV backups, log structured events through a custom hierarchy, and provide a full pytest test suite with 95%+ coverage.

---

## 📋 Functional Requirements

### 1. Descriptor Validation & Polymorphic Hierarchy (`ledger.py`)
- `PositiveAmount`: Non-data/data descriptor ensuring amounts are strictly positive numbers.
- `ISO8601Timestamp`: Descriptor ensuring ISO-8601 compliant UTC timestamps.
- Abstract base class `LedgerEntry(ABC)` with subclass implementations:
  - `TransferEntry`: contains `from_account`, `to_account`, `amount`.
  - `FeeEntry`: contains `account_id`, `fee_type`, `amount`.
- Cooperative multiple inheritance with `AuditMixin` ensuring all state changes trigger `super().log()`.

### 2. Context Management & Custom Decorators
- `@rate_limited(max_per_second: int)`: Decorator protecting ledger writes with token bucket or sliding window.
- `AtomicLedgerTransaction`: Context manager supporting `with ledger.transaction() as tx:`.
  - Commits all entries on clean exit.
  - Automatically rolls back and restores previous state on exception.
  - Correctly re-raises exceptions without swallowing.

### 3. Serialization & Atomic File I/O
- `export_snapshot(path: Path, format: str)`: Atomic writes using temporary staging files replaced via `os.replace`.
- Fully handles non-ASCII characters with explicit `encoding="utf-8"`.

### 4. Pytest Verification Suite (`test_ledger.py`)
- Minimum 10 automated unit tests.
- Parameterized tests covering boundary conditions.
- Uses `pytest.approx` on all monetary assertions.
- Zero test order dependence.

---

## 📊 Grading Rubric (100 Points Total)

| Requirement | Criteria | Points |
| :--- | :--- | :--- |
| **Deep OOP & Descriptors** | Clean descriptor protocols (`__set_name__`, validation), sound MRO | 25 pts |
| **Decorators & Context Managers** | `@wraps` preserved; atomic rollback on failure; exception bubbling | 20 pts |
| **Atomic Serialization** | Staging file rename prevents corrupt files on sudden abort; UTF-8 verified | 20 pts |
| **Error Handling & Chaining** | Custom domain exceptions; explicit `raise ... from err`; zero bare excepts | 15 pts |
| **Testing Quality** | 10+ tests, 95%+ line coverage, fixtures isolate module state cleanly | 20 pts |

**Passing Threshold:** 85/100 points required to advance to Phase 3.

---

## 🚦 Pre-Flight Gate

**Do not start this exam until all of the following pass.** Attempting a
checkpoint on a foundation that does not build wastes the exam — you will spend
your time debugging setup instead of demonstrating skill.

```bash
# From the course root. All must be green.
pytest Module_04_Deep_OOP \
      Module_05_Decorators_Generators_Context_Managers \
      Module_06_Error_Handling_Logging \
      Module_07_Files_Data_Formats_Serialization \
      Module_08_Testing_Quality_Assurance \
      -q

python tools/check_links.py --quiet
ruff check .
```

If any of that is red, fix it first. The exam assumes a working environment.

---

## 📏 Exam Rules

| Rule | Detail |
| :--- | :--- |
| **Time box** | Set a timer. When it ends, stop and submit what you have. |
| **No solution exists** | There is deliberately no reference implementation for this exam. The rubric is the specification. |
| **Modules are open-book** | Re-read any README, demo or troubleshooting guide. That is not cheating; it is what the job looks like. |
| **`project_solution/` is closed-book** | Do not read the module solutions during the exam. Copying them measures nothing. |
| **Write your own tests** | Untested code scores zero on the correctness criteria, however elegant it looks. |
| **Working beats complete** | A subset that runs and is tested outscores a full implementation that does not import. |

---

## 🔬 Self-Verification Harness

Produce this evidence before you score yourself. An unmeasured claim earns no
points.

```bash
# 1. It imports and runs at all
python -m your_solution            # must not traceback

# 2. Your tests pass
pytest your_tests.py -v            # paste the summary line

# 3. It is clean
ruff check .
mypy --strict your_solution.py     # advisory, but note the count

# 4. Coverage of your own code
pytest --cov=your_solution --cov-report=term-missing
```

Record the four outputs. The rubric below is scored against **evidence**, not
against intent.

---

## ⏱️ If You Run Out of Time

Score what exists and be honest about the gap. Partial credit is real:

1. **Submit the working subset.** Delete or clearly comment out anything that
   does not run — a broken import costs you every point in the file.
2. **Write down what is missing**, in one line per requirement. Naming your own
   gap accurately is itself a senior skill and earns the analysis criteria.
3. **Keep your tests.** Tests for the parts you finished are worth more than
   untested code for the parts you did not.

---

## 🔁 If You Score Below the Threshold

This is diagnostic information, not a verdict. Do exactly this:

1. Identify which **rubric row** you lost the most points on.
2. Go back to: **Module 04's MRO material and Module 08's testing patterns**.
3. Work that module's `debug_lab/` — it drills the failure modes this exam
   punishes.
4. Re-take the exam with a different data set or a changed requirement so you
   are re-solving rather than remembering.

Re-taking a checkpoint is normal. Advancing past one you failed is not — every
later phase assumes this one.

---

## 🎓 What This Checkpoint Actually Measures

Modules 04–08 taught you a set of tools. This exam tests **whether you can design types that hold their invariants and prove it with tests you wrote yourself**.

That is deliberately different from the module quizzes, which test whether you
understood each piece. Here nobody tells you which tool to reach for. Choosing
correctly, under a time limit, with no solution to check against, is the whole
point — and it is the closest this course gets to the actual job.
