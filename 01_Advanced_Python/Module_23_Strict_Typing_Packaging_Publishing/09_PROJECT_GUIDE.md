# Module_23_Strict_Typing_Packaging_Publishing: Project Implementation Guide

**Deliverable:** a strictly typed enterprise API client library adhering to mypy --strict, typing.Protocol, and modern pyproject.toml packaging.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_typed_sdk.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Protocol Definitions
Implement `@runtime_checkable` `TransportProtocol` defining the `send_request` contract without concrete inheritance.

### Step 2 — Generic Response Envelope
Implement `ApiResponse[T]` as an immutable frozen dataclass parameterizable across arbitrary payload types.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_typed_sdk.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Typed Enterprise Client
Implement `TypedEnterpriseClient` accepting `TransportProtocol` and applying type transforms to raw response dictionaries.

### Step 4 — Strict Typing & py.typed Marker
Ensure zero type errors under `mypy --strict` and include the `py.typed` marker file for downstream type distribution.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/typed_sdk.py`, change `ApiResponse` to a mutable dataclass (`@dataclass` without `frozen=True`).
Run:
```bash
pytest ../project_solution/test_typed_sdk.py -k test_api_response_immutability -v
```
Watch the test fail when `resp.status_code` can be mutated, then restore `frozen=True`.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_typed_sdk.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Async Transport Protocol:** Define `AsyncTransportProtocol` and build `AsyncTypedEnterpriseClient`.
2. **Pydantic Response Transform:** Integrate Pydantic `TypeAdapter[T]` for automatic payload parsing.
3. **Automated Wheel Build Pipeline:** Configure GitHub Actions workflow building and validating wheels with `build` and `twine`.
4. **Covariant Generics:** Implement a covariant generic read-only repository protocol `Repository[+T_co]`.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_transport_protocol_conformance` | Proves mock transport satisfies TransportProtocol interface |
| `test_typed_client_successful_fetch` | Proves client fetches data and transforms raw dict into UserDTO |
| `test_typed_client_404_error_handling` | Proves lookup errors return 404 ApiResponse without crashing |
| `test_api_response_is_success_property` | Proves is_success evaluates correctly across 2xx, 4xx, and 5xx |
| `test_api_response_immutability` | Proves ApiResponse is frozen and prevents attribute modification |

---

## 🎓 You have mastered this module when you can…

- [ ] Configure and pass mypy --strict with zero type errors or suppressions
- [ ] Use typing.Protocol and @runtime_checkable for structural subtyping (duck typing)
- [ ] Design generic classes and functions using TypeVar, Generic[T], and ParamSpec
- [ ] Explain variance: invariant, covariant (+T_co), and contravariant (-T_contra)
- [ ] Create immutable data transfer objects using frozen dataclasses
- [ ] Package a typed Python library with pyproject.toml and the py.typed marker
- [ ] Write unit tests verifying both runtime behavior and static type contracts
