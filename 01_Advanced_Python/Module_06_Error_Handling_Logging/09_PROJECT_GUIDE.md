# Module_06_Error_Handling_Logging: Project Implementation Guide

**Deliverable:** an enterprise checkout microservice with custom domain exception hierarchies, explicit exception chaining, and structured logging.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_checkout_service.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Domain Exception Hierarchy
Define `CheckoutError(Exception)` as base class, with specialized subclasses `InventoryUnavailableError`, `PaymentDeclinedError`, and `FraudCheckFailedError`.

### Step 2 — Structured Logger Configuration
Configure hierarchical logger with contextual formatting (timestamp, request ID, severity, message).

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_checkout_service.py -k "basic or initial or health or create" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Exception Chaining
Implement checkout transaction wrapping low-level network and parsing failures with `raise PaymentDeclinedError(...) from err`.

### Step 4 — Retry Logic with Backoff
Implement retry handler for transient errors while failing fast on permanent domain rejections.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/checkout_service.py`, remove `from err` when re-raising a low-level error as `PaymentDeclinedError`.
Run:
```bash
pytest ../project_solution/test_checkout_service.py -k test_exception_chaining_preserves_cause -v
```
Watch the test fail when `exc.__cause__` evaluates to `None`, then restore the explicit chaining.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_checkout_service.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Distributed Trace Context:** Inject OpenTelemetry-compatible W3C traceparent headers into all log records.
2. **Circuit Breaker:** Implement a circuit breaker pattern opening after 5 consecutive gateway timeouts.
3. **Dead Letter Alerting:** Send unrecoverable exceptions to a simulated webhook alert sink.
4. **Audit Sentry Integration:** Configure custom exception hooks using `sys.excepthook` for uncaught panics.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_checkout_success_path` | Proves valid transactions complete and log success metrics |
| `test_inventory_unavailable_raises_domain_error` | Proves out-of-stock items raise InventoryUnavailableError |
| `test_exception_chaining_preserves_cause` | Proves __cause__ preserves root low-level exception trace |
| `test_structured_log_contains_trace_id` | Proves log lines include correlation IDs and timestamps |
| `test_bare_except_eliminated` | Proves KeyboardInterrupt and system signals are not swallowed |

---

## 🎓 You have mastered this module when you can…

- [ ] Design clean domain exception hierarchies extending Exception (never BaseException)
- [ ] Use explicit exception chaining with raise ... from to preserve root cause context
- [ ] Configure logging handlers, formatters, and filters cleanly without duplicate lines
- [ ] Avoid bare except: blocks that swallow KeyboardInterrupt and SystemExit
- [ ] Use sys.exc_info() and traceback module for detailed error diagnosis
- [ ] Implement retry loops with exponential backoff for transient failures
- [ ] Test failure paths and exception assertions rigorously with pytest.raises
