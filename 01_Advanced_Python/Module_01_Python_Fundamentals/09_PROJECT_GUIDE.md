# Module_01_Python_Fundamentals: Project Implementation Guide

**Deliverable:** a high-precision financial calculation engine and interactive CLI calculator with complete amortization schedules.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_calculator.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Compound Interest Formula
Implement `calculate_compound_interest(principal, annual_rate_percent, years, compounds_per_year)` using standard decimal rates:
$$A = P \left(1 + \frac{r}{n}\right)^{n \cdot t}$$

### Step 2 — Fixed Monthly Loan Payment
Implement `calculate_monthly_loan_payment(principal, annual_rate_percent, years)` handling the zero-interest edge case.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_calculator.py -k "basic or initial or health or create" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Loan Amortization Schedule
Implement `generate_amortization_schedule` iterating through each monthly payment, computing interest, principal decrement, and zeroing out remaining balance.

### Step 4 — Interactive CLI with match-case
Construct the CLI menu supporting input validation for non-negative monetary figures and tabular output.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/calculator.py`, change the zero-interest check `if annual_rate_percent == 0.0:` to return `0.0` instead of `principal / total_months`.
Run:
```bash
pytest ../project_solution/test_calculator.py -k test_loan_monthly_payment_zero_interest -v
```
Watch the test fail with `0.0 != 1000.0`, then restore the proper division logic and verify it passes.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_calculator.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Decimal Precision Mode:** Refactor calculations using Python's `decimal.Decimal` with configurable rounding context.
2. **Extra Principal Payments:** Add support for one-time or recurring extra principal prepayments.
3. **Inflation Adjustment:** Implement real purchasing-power calculation using historical CPI indices.
4. **CSV Export:** Export complete amortization schedules to RFC-4180 compliant CSV files.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_compound_interest_monthly` | Proves compound interest calculation matches financial spec |
| `test_loan_monthly_payment_standard` | Proves fixed monthly amortization payment calculation is accurate |
| `test_loan_monthly_payment_zero_interest` | Proves zero-interest loan edge case is handled cleanly |
| `test_amortization_schedule_completes_to_zero` | Proves amortization table correctly zeroes out remaining balance |
| `test_amortization_schedule_total_principal_paid` | Proves sum of monthly principal payments equals loan principal |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain IEEE-754 floating-point limitations and why 0.1 + 0.2 != 0.3
- [ ] Choose correctly between float, int cents, and Decimal for financial applications
- [ ] Implement robust input validation loops without recursion
- [ ] Use match-case structural pattern matching effectively
- [ ] Format currency strings cleanly using f-strings with thousands separators
- [ ] Formulate and generate amortization tables with zero final balance
- [ ] Write unit tests verifying numerical formulas against known reference vectors
