# Design Rationale: Financial Calculator & Amortization Engine

## Architectural Overview
A high-precision financial calculator computing compound savings interest and monthly loan amortization schedules using Python 3.10+ `match-case` control flow, decimal rounding, and defensive numeric validation.

## Key Design Decisions
1. **Discrete Monthly Rate Scaling:** Financial interest rates are computed per period ($i = r / 12 / 100$) before exponential compounding, avoiding cumulative precision drift across multi-year amortization schedules.
2. **Loop-Based Non-Crashing Prompts:** User input validation uses explicit sentinel loops with `try-except ValueError` rather than recursive prompts, avoiding stack overflow on repeated invalid inputs.
3. **Formatted Tabular Projections:** Amortization schedules emit structured dictionaries separated from presentation formatting, allowing the calculation engine to be reused in web APIs or GUIs.

## Rejected Alternatives
1. **Floating-Point Equality Checks (`balance == 0.0`):**
   - *Reason for Rejection:* IEEE 754 binary floating-point representation causes fractional cents to drift (e.g., `$0.00000000000004`), resulting in infinite loops when checking zero loan balances.
2. **Recursive Input Prompts (`prompt_user()` calling itself on error):**
   - *Reason for Rejection:* Malicious or automated bad inputs cause Python recursion limits (`RecursionError`) to terminate the process after 1,000 attempts.

## Invariants & Guarantees
- Monetary amounts rounded to 2 decimal places at reporting boundaries.
- Principal reduction and interest paid strictly sum to total monthly payment.

## Verification
```bash
pytest test_calculator.py -v
```

---

## 🗺️ Recommended Step-by-Step Project Study Path

Follow this sequence to analyze and master the project architecture:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Architecture Review** | Read the specification and design breakdown in this `README.md`. |
| **2** | **Examine Implementation** | Study modular design patterns and invariant safeguards across source files. |
| **3** | **Run Test Suite** | Execute `pytest tests/` to see all production test cases pass green. |
| **4** | **Independent Re-Build** | Re-implement the solution from scratch in `[../starter/](../starter/)` until all tests pass. |

