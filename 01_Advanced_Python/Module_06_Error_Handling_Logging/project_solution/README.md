# Design Rationale: Resilient E-Commerce Checkout & Audit Logger

## Architectural Overview
A fault-tolerant checkout processing service featuring a domain exception hierarchy, explicit exception chaining (`raise from`), and structured JSON event logging.

## Key Design Decisions
1. **Explicit Root Cause Chaining:** Low-level network and database errors are re-raised as high-level domain exceptions (`PaymentFailedError`) using `raise ... from exc`, preserving full debug stack traces.
2. **Structured JSON Telemetry:** All logs are emitted as single-line JSON objects with timestamps, correlation IDs, and context parameters for automated ingestion into log aggregators.
3. **Granular Domain Hierarchy:** Custom exceptions inherit from a common `CheckoutError` base class, allowing clients to catch either specific errors or all checkout failures.

## Rejected Alternatives
1. **Bare `except:` or Catch-All `except Exception:` Blocks:**
   - *Reason for Rejection:* Catching broad exceptions swallows developer typos (`NameError`), syntax bugs, and system signals (`KeyboardInterrupt`).
2. **Formatting Unstructured String Logs (`f"Error {e} occurred"`):**
   - *Reason for Rejection:* Unstructured string logs require fragile regex to parse in production APM tools and cannot be indexed by user ID or transaction ID.

## Invariants & Guarantees
- No exception is caught without either handling, logging, or re-raising with context.
- Log entries are valid JSON payloads.

## Verification
```bash
pytest test_checkout_service.py -v
```
