# Design Rationale: Zero-Copy Binary Protocol Engine & Model DSL

## Architectural Overview
An advanced Python metaprogramming engine implementing custom typed Data Descriptors, class customization hooks via `__init_subclass__`, and zero-copy binary slicing with `memoryview`.

## Key Design Decisions
1. **Typed Data Descriptors:** Implements `__set__` and `__get__` to intercept attribute access, storing validated state directly inside `instance.__dict__` without instance state bleeding.
2. **Modern Class Hooks via `__init_subclass__`:** Replaces complex metaclasses with PEP 487 hooks for declarative schema and table registration, eliminating metaclass MRO conflicts.
3. **Zero-Copy Memoryview Buffers:** Parses massive binary network payloads using `memoryview` slices, avoiding memory reallocation and copying.

## Rejected Alternatives
1. **Storing Descriptor State on `self.value`:**
   - *Reason for Rejection:* Storing values on the descriptor instance causes all host class instances to share the exact same value like a global variable.
2. **Using Metaclasses for Simple Registry Systems:**
   - *Reason for Rejection:* Custom metaclasses complicate multiple inheritance and trigger `metaclass conflict` exceptions when inheriting across third-party libraries.

## Invariants & Guarantees
- Data descriptors strictly take precedence over instance dictionary lookup.
- Zero memory allocations during binary buffer slicing.

## Verification
```bash
pytest test_mini_orm.py -v
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

