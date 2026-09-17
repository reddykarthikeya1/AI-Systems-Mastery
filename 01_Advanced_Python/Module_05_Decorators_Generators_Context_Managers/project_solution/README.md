# Design Rationale: Streaming Log Analyzer & Execution Profiler

## Architectural Overview
A memory-efficient streaming analytics pipeline that parses and filters gigabyte-scale access logs using generator pipelines, stacked decorators (`@retry`, `@timed`), and context managers.

## Key Design Decisions
1. **Zero-RAM Generator Pipelines:** Log parsing, timestamp filtering, and status code aggregation are chained as generator iterators, keeping memory consumption constant ($O(1)$, ~200 bytes) regardless of file size.
2. **Metadata-Preserving Decorators:** All wrapper decorators use `@functools.wraps`, preserving function names, docstrings, and type annotations for APM profilers.
3. **Bracketed Resource Management:** File reading and profiling spans use custom context managers, guaranteeing descriptor closing even when parsing fails mid-stream.

## Rejected Alternatives
1. **Loading Complete Log Files into Memory (`readlines()` / List Comprehensions):**
   - *Reason for Rejection:* Ingesting a 10 GB access log allocates gigabytes of `PyObject*` pointers, exhausting server RAM and triggering OS OOM killers.
2. **Stateful Class Iterators for Simple Transformations:**
   - *Reason for Rejection:* Writing classes with `__iter__` and `__next__` for every filter adds 5x boilerplate compared to composable `yield` functions.

## Invariants & Guarantees
- Memory usage remains strictly flat across multi-gigabyte files.
- Wrapped functions preserve original signatures for inspection.

## Verification
```bash
pytest test_log_analyzer.py -v
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

