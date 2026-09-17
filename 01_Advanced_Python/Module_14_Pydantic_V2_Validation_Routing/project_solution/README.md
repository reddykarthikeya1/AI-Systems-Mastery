# Design Rationale: Healthcare Patient Ingestion & Validation API

## Architectural Overview
A high-integrity healthcare API leveraging Pydantic V2's compiled Rust core (`pydantic-core`), strict field validators, cross-field model validators, and discriminated unions.

## Key Design Decisions
1. **Tagged Discriminated Unions:** Polymorphic event payloads (Lab Results, Vitals, Prescriptions) are dispatched using discriminator tags, executing in $O(1)$ time without trial-and-error union parsing.
2. **`mode='after'` Model Validators:** Cross-field domain invariants (e.g., discharge date occurring strictly after admission date) are evaluated on typed instances, ensuring clean domain exceptions.
3. **`strict=True` Boundary Enforcement:** Prevents silent lossy type coercion (such as strings or floats implicitly truncating into integers) on medical dosage measurements.

## Rejected Alternatives
1. **Untagged `Union[LabResult, Prescription, Note]` Types:**
   - *Reason for Rejection:* Sequential union evaluation tries each schema in order, introducing high parsing latency and producing ambiguous error messages on invalid fields.
2. **Executing Database Queries Inside Validators:**
   - *Reason for Rejection:* Running I/O inside Pydantic validators violates separation of concerns, degrades validation performance, and breaks serialization purity.

## Invariants & Guarantees
- Strict type conformance with zero implicit lossy coercion.
- Polymorphic deserialization guaranteed deterministic in $O(1)$ time.

## Verification
```bash
pytest test_patient_api.py -v
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

