"""Unit tests for the Healthcare Patient Intake Microservice API."""

from __future__ import annotations

from fastapi.testclient import TestClient
from patient_api import app

client = TestClient(app)


def test_valid_patient_intake_payload() -> None:
    payload = {
        "mrn": "MRN-12345",
        "full_name": "Eleanor Vance",
        "age": 42,
        "height_cm": 168.0,
        "weight_kg": 68.5,
        "systolic_bp": 118,
        "diastolic_bp": 76,
    }
    res = client.post("/patients", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["mrn"] == "MRN-12345"
    assert data["bmi"] == 24.27
    assert data["observations"] == []


def test_invalid_mrn_format_fails_validation() -> None:
    payload = {
        "mrn": "INVALID-123",  # Must be MRN-XXXXX
        "full_name": "Luke Sanderson",
        "age": 30,
        "height_cm": 180.0,
        "weight_kg": 75.0,
        "systolic_bp": 120,
        "diastolic_bp": 80,
    }
    res = client.post("/patients", json=payload)
    assert res.status_code == 422


def test_invalid_blood_pressure_relation_fails_model_validator() -> None:
    # Systolic must be strictly greater than diastolic
    payload = {
        "mrn": "MRN-54321",
        "full_name": "Theodora Crain",
        "age": 28,
        "height_cm": 172.0,
        "weight_kg": 62.0,
        "systolic_bp": 80,
        "diastolic_bp": 120,  # Invalid: diastolic higher than systolic
    }
    res = client.post("/patients", json=payload)
    assert res.status_code == 422


def test_polymorphic_observations_discriminated_union() -> None:
    # First ensure patient exists
    intake = {
        "mrn": "MRN-88888",
        "full_name": "Nell Crain",
        "age": 26,
        "height_cm": 165.0,
        "weight_kg": 55.0,
        "systolic_bp": 110,
        "diastolic_bp": 70,
    }
    client.post("/patients", json=intake)

    # Post Lab Observation
    lab_obs = {
        "obs_type": "lab",
        "test_name": "Serum Potassium",
        "result_value": 4.2,
        "reference_range": "3.5 - 5.0 mEq/L",
    }
    res1 = client.post("/patients/MRN-88888/observations", json=lab_obs)
    assert res1.status_code == 200
    assert len(res1.json()["observations"]) == 1

    # Post Radiology Observation
    rad_obs = {
        "obs_type": "radiology",
        "modality": "MRI",
        "findings": "Normal brain parenchyma without acute infarction.",
    }
    res2 = client.post("/patients/MRN-88888/observations", json=rad_obs)
    assert res2.status_code == 200
    assert len(res2.json()["observations"]) == 2


def test_duplicate_mrn_registration_rejected() -> None:
    """Test registering duplicate MRN returns 409 Conflict."""
    payload = {
        "mrn": "MRN-99999",
        "full_name": "Unique User",
        "age": 30,
        "height_cm": 175.0,
        "weight_kg": 70.0,
        "systolic_bp": 120,
        "diastolic_bp": 80,
    }
    res1 = client.post("/patients", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/patients", json=payload)
    assert res2.status_code == 409


def test_get_patient_by_mrn() -> None:
    """Test retrieving existing patient by MRN returns 200 with record."""
    payload = {
        "mrn": "MRN-11111",
        "full_name": "Retrieve Me",
        "age": 45,
        "height_cm": 165.0,
        "weight_kg": 60.0,
        "systolic_bp": 110,
        "diastolic_bp": 70,
    }
    client.post("/patients", json=payload)
    res = client.get("/patients/MRN-11111")
    assert res.status_code == 200
    assert res.json()["full_name"] == "Retrieve Me"


def test_get_nonexistent_patient_returns_404() -> None:
    """Test looking up missing MRN returns 404."""
    res = client.get("/patients/MRN-NOTFOUND")
    assert res.status_code == 404


def test_invalid_age_out_of_bounds() -> None:
    """Test negative age or age over 120 triggers 422 validation error."""
    base = {
        "mrn": "MRN-22222",
        "full_name": "Test Age",
        "height_cm": 170.0,
        "weight_kg": 70.0,
        "systolic_bp": 120,
        "diastolic_bp": 80,
    }
    res_neg = client.post("/patients", json={**base, "age": -1})
    assert res_neg.status_code == 422

    res_huge = client.post("/patients", json={**base, "age": 150})
    assert res_huge.status_code == 422


def test_invalid_height_and_weight_bounds() -> None:
    """Test non-positive height or weight triggers 422."""
    base = {
        "mrn": "MRN-33333",
        "full_name": "Test Bounds",
        "age": 25,
        "systolic_bp": 120,
        "diastolic_bp": 80,
    }
    res = client.post("/patients", json={**base, "height_cm": 0, "weight_kg": 60.0})
    assert res.status_code == 422


def test_add_observation_to_nonexistent_patient_returns_404() -> None:
    """Test posting observation for unregistered MRN returns 404."""
    lab_obs = {
        "obs_type": "lab",
        "test_name": "Glucose",
        "result_value": 95.0,
        "reference_range": "70-99 mg/dL",
    }
    res = client.post("/patients/MRN-NONEXIST/observations", json=lab_obs)
    assert res.status_code == 404
