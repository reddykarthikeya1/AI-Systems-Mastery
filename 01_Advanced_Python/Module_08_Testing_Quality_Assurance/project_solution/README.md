# Design Rationale: Pytest Ledger Verification & QA Suite

## Architectural Overview
An enterprise-grade test architecture demonstrating scoped dependency injection fixtures, safe mocking with `autospec`, parameterized test matrices, and property-based fuzzing.

## Key Design Decisions
1. **Yield Fixtures for Resource Isolation:** Test state (temporary directories, database records) is managed via generator fixtures with guaranteed post-yield teardown, ensuring 100% test isolation.
2. **Strict Mocking with `autospec=True`:** Mocks are specced against target classes, immediately catching misspelled method names that would silently pass on unspecced mocks.
3. **`pytest.approx` for Financial Invariants:** Floating-point assertions use relative tolerance comparisons, preventing false failures from binary IEEE 754 precision noise.

## Rejected Alternatives
1. **Patching Definition Sites Instead of Lookup Sites:**
   - *Reason for Rejection:* Patching `service.send_email` when `worker.py` does `from service import send_email` fails because the worker retains the un-mocked pointer.
2. **`time.sleep()` for Concurrent Test Synchronization:**
   - *Reason for Rejection:* Arbitrary sleep durations introduce severe test suite flakiness on resource-constrained continuous integration (CI) runners.

## Invariants & Guarantees
- Zero state leakage between test functions.
- Test suites run deterministically in parallel (`pytest -n auto`).

## Verification
```bash
pytest test_ledger.py -v
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

