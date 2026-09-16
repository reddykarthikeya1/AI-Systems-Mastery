# Module_14_Pydantic_V2_Validation_Routing: Project Implementation Guide

**Deliverable:** a healthcare diagnostic API using Pydantic V2 advanced validators, discriminated unions, computed fields, and APIRouter.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_patient_api.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Patient Intake Schema
Define `PatientIntake` validating format `MRN-XXXXX` using `@field_validator`.

### Step 2 — Model Validator & Computed Fields
Implement `@model_validator(mode='after')` ensuring systolic BP > diastolic BP, and `@computed_field` for BMI calculation.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_patient_api.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Polymorphic Diagnostic Observations
Define `LabObservation` and `RadiologyObservation` using a discriminated union `Annotated[Union, Field(discriminator='obs_type')]`.

### Step 4 — APIRouter Registration
Implement `patient_router` with prefix `/patients` and integrate into root `FastAPI` application.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/patient_api.py`, remove the `@model_validator` that ensures systolic BP > diastolic BP.
Run:
```bash
pytest ../project_solution/test_patient_api.py -k test_invalid_blood_pressure_relation_fails_model_validator -v
```
Watch the test fail when inverted blood pressure is accepted, then restore the validation check.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_patient_api.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Custom Pydantic Datatypes:** Create an `MRN` type using `Annotated` with custom serialization rules.
2. **Audit Observation History:** Track observation timestamps and enforce chronological ordering.
3. **Selective Partial Updates:** Implement `PATCH /patients/{mrn}` using Pydantic partial model validation.
4. **JSON Schema Export:** Export patient data contract as standard JSON Schema for frontend client generation.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_valid_patient_intake_payload` | Proves valid patient records compute BMI and initialize observations |
| `test_invalid_mrn_format_fails_validation` | Proves malformed MRN strings fail field validation with 422 |
| `test_invalid_blood_pressure_relation` | Proves inverted blood pressure fails model validation with 422 |
| `test_polymorphic_observations_discriminated_union` | Proves discriminated union accepts both lab and radiology observations |
| `test_duplicate_mrn_registration_rejected` | Proves duplicate MRN intake returns 409 Conflict |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain Pydantic V2 core architecture and Rust-backed pydantic-core speedups
- [ ] Use @field_validator and @model_validator with mode='before' and mode='after'
- [ ] Create dynamic calculated properties using @computed_field
- [ ] Implement polymorphic data models using discriminated unions (Field(discriminator=...))
- [ ] Modularize large web applications using FastAPI APIRouter
- [ ] Prevent post-initialization mutation bugs with validate_assignment=True
- [ ] Write comprehensive API test suites covering edge cases and validation failures
