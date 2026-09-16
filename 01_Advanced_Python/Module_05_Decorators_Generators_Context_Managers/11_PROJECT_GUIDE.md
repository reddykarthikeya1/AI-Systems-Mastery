# Module_05_Decorators_Generators_Context_Managers: Project Implementation Guide

**Deliverable:** a high-throughput log analysis pipeline utilizing streaming generator pipelines, profiling decorators, and transaction context managers.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_log_analyzer.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Profiling Decorator
Implement `@profile_execution` recording function runtime, call counts, and preserving metadata with `@functools.wraps`.

### Step 2 — Streaming Generator Pipeline
Implement generator functions `read_logs`, `filter_level`, and `parse_records` processing millions of lines with \(O(1)\) memory.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_log_analyzer.py -k "basic or initial or health or create" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Safe File Context Manager
Implement `TemporaryLogSandbox` context manager provisioning temporary workspace and guaranteeing cleanup in `__exit__`.

### Step 4 — Pipeline Aggregations
Implement generator consumer aggregating status code frequencies and endpoint error rates.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/log_analyzer.py`, remove `@functools.wraps(func)` from the profiling decorator.
Run:
```bash
pytest ../project_solution/test_log_analyzer.py -k test_profiler_metadata_preservation -v
```
Watch the test fail when `func.__name__` reports `'wrapper'` instead of the decorated function's name.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_log_analyzer.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Asynchronous Streaming:** Convert the generator pipeline to async generators (`async for line in read_logs_async`).
2. **Sliding Window Rate Calculator:** Compute rolling requests-per-minute across timestamped log streams.
3. **Regex Pattern Cache:** Implement an LRU cache decorator caching compiled regular expressions.
4. **Context Manager Re-entrancy:** Ensure context manager is safely re-entrant across multiple nested with blocks.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_log_pipeline_streaming_throughput` | Proves log generator pipelines stream records without loading whole file |
| `test_profiler_metadata_preservation` | Proves @profile_execution decorator preserves docstrings and names |
| `test_filter_level_partitions_warnings` | Proves log level filtering correctly isolates ERROR and WARNING levels |
| `test_temporary_sandbox_cleanup` | Proves context manager cleans up filesystem artifacts on exit |
| `test_empty_log_stream_safe` | Proves empty log sources do not raise StopIteration or crash |

---

## 🎓 You have mastered this module when you can…

- [ ] Write parameterized and non-parameterized decorators using functools.wraps
- [ ] Chain generator expressions to build lazy streaming data processing pipelines
- [ ] Implement context managers using the __enter__ and __exit__ protocol
- [ ] Explain when __exit__ should return True vs False regarding exception suppression
- [ ] Avoid generator exhaustion traps when streams require multiple passes
- [ ] Use contextlib.contextmanager to convert generator functions into context managers
- [ ] Measure and minimize memory consumption in streaming I/O workflows
