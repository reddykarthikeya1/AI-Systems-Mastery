"""Module 08: Pytest Basics, Parametrization & Fixtures Demonstration.

Run with: pytest 01_pytest_basics_and_fixtures_demo.py -v
"""

from __future__ import annotations

from pathlib import Path

import pytest


def calculate_shipping_tier(weight_kg: float) -> str:
    """Classifies shipping cost category based on package weight."""
    if weight_kg <= 0:
        raise ValueError("Weight must be positive.")
    if weight_kg <= 1.0:
        return "STANDARD"
    if weight_kg <= 10.0:
        return "EXPRESS"
    return "FREIGHT"


# 1. Parametrized Table-Driven Test Suite
@pytest.mark.parametrize("weight, expected_tier", [
    (0.5, "STANDARD"),
    (1.0, "STANDARD"),
    (5.0, "EXPRESS"),
    (10.0, "EXPRESS"),
    (25.0, "FREIGHT"),
])
def test_shipping_tier_classification(weight: float, expected_tier: str) -> None:
    assert calculate_shipping_tier(weight) == expected_tier


def test_invalid_weight_raises_error() -> None:
    with pytest.raises(ValueError):
        calculate_shipping_tier(-2.5)


# 2. Pytest Setup and Yield Teardown Fixture
@pytest.fixture
def isolated_scratch_file(tmp_path: Path):
    """Fixture creating an isolated scratch file and ensuring cleanup."""
    file = tmp_path / "scratch_fixture.txt"
    file.write_text("INITIAL_STATE", encoding="utf-8")

    yield file  # Yield file to test function

    # Teardown execution
    if file.exists():
        file.unlink()


def test_fixture_file_lifecycle(isolated_scratch_file: Path) -> None:
    assert isolated_scratch_file.exists()
    assert isolated_scratch_file.read_text(encoding="utf-8") == "INITIAL_STATE"
    isolated_scratch_file.write_text("MUTATED_STATE", encoding="utf-8")
    assert isolated_scratch_file.read_text(encoding="utf-8") == "MUTATED_STATE"
