# Module_08_Testing_Quality_Assurance: Project Implementation Guide

**Deliverable:** a comprehensive test harness demonstrating pytest fixtures, parameterization, mocking, property-based testing with Hypothesis, and coverage analysis.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_ledger.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Test Fixtures & Isolation
Create scoped pytest fixtures ensuring test state is completely isolated and resets between test runs.

### Step 2 — Parameterized Testing
Implement `@pytest.mark.parametrize` testing boundary inputs, negative values, and zero conditions.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_ledger.py -k "basic or initial or health or create" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Property-Based Testing with Hypothesis
Write Hypothesis `@given` strategies testing universal mathematical properties (e.g. `deposit(x); withdraw(x) == initial`).

### Step 4 — Mocking External Dependencies
Use `unittest.mock` (`patch`, `MagicMock`) to simulate external banking networks and API timeouts.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/ledger.py`, change balance subtraction in `withdraw` so it subtracts `amount * 1.01` (simulating a hidden fee).
Run:
```bash
pytest ../project_solution/test_ledger.py -k test_deposit_withdraw_property -v
```
Watch Hypothesis discover the exact shrinking counterexample, then restore the balance equation.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_ledger.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Custom Hypothesis Strategies:** Define custom Hypothesis composite strategies generating valid credit card tokens.
2. **Mutation Testing:** Run `mutmut` against the test suite and eliminate all surviving mutants.
3. **Benchmark Regression Testing:** Add `pytest-benchmark` asserting algorithmic time complexity.
4. **Coverage Enforcement:** Configure `--cov-fail-under=95` ensuring high branch coverage in CI.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_ledger_deposit_and_withdraw` | Proves ledger correctly tracks account balances |
| `test_parameterized_invalid_amounts` | Proves parameterized inputs reject zero and negative values |
| `test_deposit_withdraw_property` | Proves Hypothesis invariant holds across arbitrary integers |
| `test_external_gateway_mocking` | Proves mock objects simulate network gateway timeouts |
| `test_floating_point_assertions_approx` | Proves floating point assertions utilize pytest.approx |

---

## 🎓 You have mastered this module when you can…

- [ ] Structure clean pytest suites with modular fixtures and clear arrange-act-assert phases
- [ ] Eliminate test order dependence and shared mutable module state
- [ ] Avoid assertion traps like asserting non-empty tuples (assert (x == y, 'msg'))
- [ ] Use pytest.approx on floating-point comparisons to prevent precision failures
- [ ] Write property-based tests using Hypothesis to find edge cases human testers miss
- [ ] Mock network dependencies cleanly using unittest.mock.patch and AsyncMock
- [ ] Interpret branch coverage reports and eliminate dead code
