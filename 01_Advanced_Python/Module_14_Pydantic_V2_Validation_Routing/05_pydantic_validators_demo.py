#!/usr/bin/env python3
"""Module 12: Pydantic V2 Field and Model Validators Demonstration.

This script demonstrates @field_validator and @model_validator in Pydantic V2.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator


class PatientIntake(BaseModel):
    medical_record_number: str = Field(..., description="Format: MRN-XXXXX")
    age: int = Field(..., ge=0, le=120)
    systolic_bp: int = Field(..., ge=50, le=250)
    diastolic_bp: int = Field(..., ge=30, le=150)

    @field_validator("medical_record_number")
    @classmethod
    def validate_mrn_format(cls, v: str) -> str:
        v = v.strip().upper()
        if not v.startswith("MRN-") or len(v) != 9 or not v[4:].isdigit():
            raise ValueError(f"MRN must match format 'MRN-12345' (Got: '{v}')")
        return v

    @model_validator(mode="after")
    def validate_blood_pressure_rationality(self) -> PatientIntake:
        if self.systolic_bp <= self.diastolic_bp:
            raise ValueError(
                f"Systolic BP ({self.systolic_bp}) must be strictly greater than diastolic BP ({self.diastolic_bp})!"
            )
        return self


def main() -> None:
    print("=" * 60)
    print("  Pydantic V2 Advanced Field & Model Validation Demo")
    print("=" * 60)

    # Valid intake
    patient = PatientIntake(
        medical_record_number=" mrn-10293 ",
        age=35,
        systolic_bp=120,
        diastolic_bp=80,
    )
    print(f"Validated Patient Intake: {patient.model_dump_json(indent=2)}")


if __name__ == "__main__":
    main()
