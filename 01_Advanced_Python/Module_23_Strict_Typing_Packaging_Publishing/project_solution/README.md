# Design Rationale: Strictly-Typed Enterprise Client SDK & Package Distribution

## Architectural Overview
A strictly-typed Python client SDK configured with `mypy --strict`, generic data structures, structural subtyping via `Protocols`, `ParamSpec` decorator preservation, and PEP 621 packaging.

## Key Design Decisions
1. **Structural Subtyping via `Protocol` (PEP 544):** Interfaces (HTTP Transports, Storage Backends) are defined as Protocols, enabling duck typing with compile-time static type verification.
2. **Decorator Type Preservation with `ParamSpec`:** Higher-order audit and retry wrappers use `ParamSpec` and `TypeVar`, preserving wrapped function argument signatures for IDE autocomplete.
3. **PEP 561 `py.typed` Marker Packaging:** Ships an inline `py.typed` marker file, ensuring downstream consumers benefit from static type checking.

## Rejected Alternatives
1. **Using `list[T]` (Invariant) for Read-Only Parameter Signatures:**
   - *Reason for Rejection:* `list[T]` is invariant; a function accepting `list[Animal]` rejects `list[Dog]`. Using `Sequence[T]` (covariant) enables clean polymorphism.
2. **Using `Any` to Suppress Complex Generic Errors:**
   - *Reason for Rejection:* Silencing errors with `Any` propagates untyped holes throughout the codebase, defeating static type verification.

## Invariants & Guarantees
- Passes `mypy --strict` with zero type ignores.
- Published wheels install cleanly across all supported platforms.

## Verification
```bash
pytest test_typed_sdk.py -v
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

