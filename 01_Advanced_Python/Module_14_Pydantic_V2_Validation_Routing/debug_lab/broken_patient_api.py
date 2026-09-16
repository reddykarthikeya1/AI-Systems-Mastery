#!/usr/bin/env python3
"""Broken Patient Validation API demonstrating post-validation mutation and model dump traps."""

from pydantic import BaseModel, Field, field_validator

class PatientRecord(BaseModel):
    mrn: str
    age: int = Field(..., ge=0, le=120)

    @field_validator("mrn")
    @classmethod
    def validate_mrn(cls, v: str) -> str:
        if not v.startswith("MRN-"):
            raise ValueError("MRN must begin with 'MRN-'")
        return v

def test_model_bypass():
    p = PatientRecord(mrn="MRN-12345", age=30)
    # Direct mutation bypasses field constraints!
    p.age = -50
    p.mrn = "INVALID"
    print(f"Bypassed validation: mrn={p.mrn}, age={p.age} (Violates age >= 0 and MRN prefix!)")

if __name__ == "__main__":
    test_model_bypass()
