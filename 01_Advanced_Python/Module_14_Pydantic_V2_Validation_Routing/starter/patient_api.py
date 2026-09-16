"""STARTER - Module 14: Pydantic V2 Validation Routing

Healthcare Patient Intake & Diagnostic Microservice API.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_patient_api.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/patient_api.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
from typing import Annotated, Literal
from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator

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
        # [Tier 1] Algorithm: Validate input arguments against constraints and
        #   raise specific exception.
        # HINTS:
        #  - Check boundary conditions (e.g. non-empty string, positive integer,
        #   range).
        #  - Raise ValueError or TypeError with actionable descriptive messages.
        # GRADES: test_invalid_mrn_format_fails_validation
        # WARNING: Never swallow validation errors or return None instead of
        #   raising.
        raise NotImplementedError("Module 14: implement PatientIntake.validate_mrn_format()")


    @model_validator(mode="after")
    def validate_blood_pressure(self) -> PatientIntake:
        # [Tier 1] Algorithm: Validate input arguments against constraints and
        #   raise specific exception.
        # HINTS:
        #  - Check boundary conditions (e.g. non-empty string, positive integer,
        #   range).
        #  - Raise ValueError or TypeError with actionable descriptive messages.
        # GRADES: test_invalid_blood_pressure_relation_fails_model_validator
        # WARNING: Never swallow validation errors or return None instead of
        #   raising.
        raise NotImplementedError("Module 14: implement PatientIntake.validate_blood_pressure()")


    @computed_field
    @property
    def bmi(self) -> float:
        # [Tier 2] Algorithm: Implement PatientIntake.bmi adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_valid_patient_intake_payload
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 14: implement PatientIntake.bmi()")



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

patient_router = APIRouter(prefix="/patients", tags=["Patients"])
patients_db: dict[str, PatientRecord] = {}

@patient_router.post("", response_model=PatientRecord, status_code=status.HTTP_201_CREATED)
def intake_patient(payload: PatientIntake) -> PatientRecord:
    # [Tier 2] Algorithm: Implement intake_patient adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_valid_patient_intake_payload
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 14: implement intake_patient()")


@patient_router.get("/{mrn}", response_model=PatientRecord)
def get_patient(mrn: str) -> PatientRecord:
    # [Tier 1] Algorithm: Implement get_patient adhering to the contract defined
    #   in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_get_patient_by_mrn
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 14: implement get_patient()")


@patient_router.post("/{mrn}/observations", response_model=PatientRecord)
def add_observation(mrn: str, obs: Observation) -> PatientRecord:
    # [Tier 2] Algorithm: Implement add_observation adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_add_observation_to_nonexistent_patient_returns_404
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 14: implement add_observation()")

app = FastAPI(
    title="Healthcare Intake & Diagnostic Microservice",
    version="2.0.0",
)
