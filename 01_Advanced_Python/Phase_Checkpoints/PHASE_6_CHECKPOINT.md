# Phase 6 Checkpoint Exam: Metaprogramming, Native Extensions & Strict Typing

> **Phase Scope:** Modules 21–23 (Metaprogramming, Rust Native Extensions, Strict Typing & Packaging)  
> **Allocated Time:** 120 Minutes  
> **Format:** Advanced systems programming, FFI, and type-system design exam.

---

## 🎯 The Exam Mission: High-Performance Declarative Data Engine

Construct a type-safe, high-speed declarative modeling framework that compiles performance-critical numeric kernels to native Rust via PyO3, verifies protocol compliance statically with `mypy --strict`, and dynamically constructs database schemas using metaprogramming descriptors.

---

## 📋 Functional Requirements

### 1. Declarative Metaprogramming (`declarative.py`)
- Base model using `__init_subclass__` for automatic field registration.
- Slotted descriptors storing state in private instance slots rather than descriptor objects.
- Automatic DDL schema generation (`CREATE TABLE ...`).

### 2. Native Rust Kernel (or CFFI / Slotted fallback)
- Compiled native function computing vector dot products or cryptographic hashes.
- Properly releases the GIL during computation with `py.allow_threads`.
- Handles integer wrapping safely.

### 3. Strict Typing & Protocols (`protocols.py`)
- Clean `@runtime_checkable` `Protocol` definitions.
- Fully typed generic response envelope `ApiResponse[T]`.
- Zero errors under `mypy --strict`.

---

## 📊 Grading Rubric (100 Points Total)

| Requirement | Criteria | Points |
| :--- | :--- | :--- |
| **Metaprogramming Integrity** | Clean `__init_subclass__`, descriptor state isolation, no global leaks | 30 pts |
| **FFI & GIL Handling** | Safe FFI boundaries, correct error mapping, measured GIL release | 30 pts |
| **Strict Typing & Protocol Design** | Generic covariance/contravariance sound; 100% clean under `mypy --strict` | 25 pts |
| **Packaging & Standards** | Modern pyproject.toml configuration with `py.typed` marker | 15 pts |

**Passing Threshold:** 85/100 points required to advance to Phase 7.

---

## 🚦 Pre-Flight Gate

**Do not start this exam until all of the following pass.** Attempting a
checkpoint on a foundation that does not build wastes the exam — you will spend
your time debugging setup instead of demonstrating skill.

```bash
# From the course root. All must be green.
pytest Module_21_Metaprogramming_Descriptors_Memory \
      Module_22_CPython_Internals_Rust_PyO3_Extensions \
      Module_23_Strict_Typing_Packaging_Publishing \
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
2. Go back to: **Module 22's escape-hatch decision table — and when NOT to go native**.
3. Work that module's `debug_lab/` — it drills the failure modes this exam
   punishes.
4. Re-take the exam with a different data set or a changed requirement so you
   are re-solving rather than remembering.

Re-taking a checkpoint is normal. Advancing past one you failed is not — every
later phase assumes this one.

---

## 🎓 What This Checkpoint Actually Measures

Modules 21–23 taught you a set of tools. This exam tests **whether you can reach into the language's machinery without making the result unmaintainable**.

That is deliberately different from the module quizzes, which test whether you
understood each piece. Here nobody tells you which tool to reach for. Choosing
correctly, under a time limit, with no solution to check against, is the whole
point — and it is the closest this course gets to the actual job.
