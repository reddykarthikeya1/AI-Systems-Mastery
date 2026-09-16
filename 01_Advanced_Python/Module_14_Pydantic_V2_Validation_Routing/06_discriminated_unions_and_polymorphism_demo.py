#!/usr/bin/env python3
"""Module 12: Discriminated Unions & Polymorphism Demonstration.

This script demonstrates parsing polymorphic JSON payloads using Pydantic V2
discriminated unions.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter


class LabTestResult(BaseModel):
    record_type: Literal["lab_test"]
    test_name: str
    numeric_value: float
    unit: str


class RadiologyReport(BaseModel):
    record_type: Literal["radiology"]
    scan_type: str  # e.g. "MRI", "X-RAY", "CT"
    findings_summary: str


# Tagged Discriminated Union
MedicalRecord = Annotated[LabTestResult | RadiologyReport, Field(discriminator="record_type")]
MedicalRecordAdapter = TypeAdapter(MedicalRecord)


def main() -> None:
    print("=" * 60)
    print("  Polymorphic Discriminated Unions Demo")
    print("=" * 60)

    raw_payload_1 = {"record_type": "lab_test", "test_name": "Blood Glucose", "numeric_value": 95.4, "unit": "mg/dL"}
    raw_payload_2 = {"record_type": "radiology", "scan_type": "MRI Brain", "findings_summary": "Normal structure."}

    rec1 = MedicalRecordAdapter.validate_python(raw_payload_1)
    rec2 = MedicalRecordAdapter.validate_python(raw_payload_2)

    print(f"Parsed Record 1: Type={type(rec1).__name__}, Value={rec1.numeric_value} {rec1.unit}")
    print(f"Parsed Record 2: Type={type(rec2).__name__}, Summary='{rec2.findings_summary}'")


if __name__ == "__main__":
    main()
