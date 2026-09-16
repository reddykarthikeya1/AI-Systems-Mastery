# Debug Lab: Module 14 — Pydantic V2 Traps

## How to Run
```bash
python debug_lab/broken_patient_api.py
```

## Observed Symptoms
1. **Validation rules silently bypassed after instantiation**:
   Setting `p.age = -50` succeeds without raising `ValidationError`, allowing invalid domain state into downstream layers.
2. **Invalid MRN prefix accepted on mutation**:
   `p.mrn = "INVALID"` succeeds silently.
