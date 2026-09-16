#!/usr/bin/env python3
"""Healthcare Patient Intake & Diagnostic Microservice API.

Module 12 (Pydantic V2 & Advanced Validation) Turnkey Project Implementation.
Demonstrates Pydantic V2 @field_validator, @model_validator, @computed_field,
Discriminated Unions, and APIRouter.
"""

from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator

# ==========================================
# 1. Pydantic V2 Schemas & Validators
# ==========================================

class PatientIntake(BaseModel):
    mrn: str = Field(..., description="Format: MRN-XXXXX")
    full_name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=0, le=120)
    height_cm: float = Field(..., gt=30.0, le=250.0)
    weight_kg: float = Field(..., gt=1.0, le=400.0)
    systolic_bp: int = Field(..., ge=50, le=260)
    diastolic_bp: int = Field(..., ge=30, le=160)

    @field_validator("mrn")
    @classmethod
    def validate_mrn_format(cls, v: str) -> str:
        clean = v.strip().upper()
        if not clean.startswith("MRN-") or len(clean) != 9 or not clean[4:].isdigit():
            raise ValueError(f"MRN must follow format 'MRN-XXXXX' with 5 digits (Got: '{v}')")
        return clean

    @model_validator(mode="after")
    def validate_blood_pressure(self) -> PatientIntake:
        if self.systolic_bp <= self.diastolic_bp:
            raise ValueError(
                f"Systolic BP ({self.systolic_bp}) must be strictly higher than diastolic BP ({self.diastolic_bp})!"
            )
        return self

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height_cm / 100.0
        return round(self.weight_kg / (height_m ** 2), 2)


# ==========================================
# 2. Polymorphic Diagnostic Observation Schemas
# ==========================================

class LabObservation(BaseModel):
    obs_type: Literal["lab"]
    test_name: str
    result_value: float
    reference_range: str


class RadiologyObservation(BaseModel):
    obs_type: Literal["radiology"]
    modality: str  # CT, MRI, Ultrasound, X-Ray
    findings: str


Observation = Annotated[LabObservation | RadiologyObservation, Field(discriminator="obs_type")]


class PatientRecord(PatientIntake):
    observations: list[Observation] = []


# ==========================================
# 3. Modular APIRouter Architecture
# ==========================================

patient_router = APIRouter(prefix="/patients", tags=["Patients"])
patients_db: dict[str, PatientRecord] = {}


@patient_router.post("", response_model=PatientRecord, status_code=status.HTTP_201_CREATED)
def intake_patient(payload: PatientIntake) -> PatientRecord:
    if payload.mrn in patients_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Patient with MRN '{payload.mrn}' already registered!",
        )
    record = PatientRecord(**payload.model_dump())
    patients_db[payload.mrn] = record
    return record


@patient_router.get("/{mrn}", response_model=PatientRecord)
def get_patient(mrn: str) -> PatientRecord:
    clean_mrn = mrn.strip().upper()
    if clean_mrn not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient '{clean_mrn}' not found",
        )
    return patients_db[clean_mrn]


@patient_router.post("/{mrn}/observations", response_model=PatientRecord)
def add_observation(mrn: str, obs: Observation) -> PatientRecord:
    clean_mrn = mrn.strip().upper()
    if clean_mrn not in patients_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient '{clean_mrn}' not found",
        )
    patient = patients_db[clean_mrn]
    patient.observations.append(obs)
    return patient


# ==========================================
# 4. Root FastAPI Application
# ==========================================

app = FastAPI(
    title="Healthcare Intake & Diagnostic Microservice",
    version="2.0.0",
)
app.include_router(patient_router)
