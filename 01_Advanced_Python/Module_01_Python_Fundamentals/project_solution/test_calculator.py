"""Unit tests for calculator.py financial calculation functions."""

from __future__ import annotations

import pytest
from calculator import (
    calculate_compound_interest,
    calculate_monthly_loan_payment,
    generate_amortization_schedule,
)


def test_compound_interest_monthly() -> None:
    """Test standard compound interest with monthly compounding ($10,000 at 5% for 10 years)."""
    balance, interest = calculate_compound_interest(
        principal=10000.0,
        annual_rate_percent=5.0,
        years=10,
        compounds_per_year=12,
    )
    assert balance == 16470.09
    assert interest == 6470.09


def test_compound_interest_annual() -> None:
    """Test compound interest with annual compounding ($1,000 at 10% for 3 years)."""
    balance, interest = calculate_compound_interest(
        principal=1000.0,
        annual_rate_percent=10.0,
        years=3,
        compounds_per_year=1,
    )
    # 1000 * 1.10^3 = 1331.00
    assert balance == 1331.00
    assert interest == 331.00


def test_compound_interest_zero_rate() -> None:
    """Test compound interest when interest rate is 0%."""
    balance, interest = calculate_compound_interest(5000.0, 0.0, 5)
    assert balance == 5000.0
    assert interest == 0.0


def test_compound_interest_negative_inputs_raise_error() -> None:
    """Test that negative inputs raise ValueError."""
    with pytest.raises(ValueError):
        calculate_compound_interest(-100.0, 5.0, 5)
    with pytest.raises(ValueError):
        calculate_compound_interest(100.0, -5.0, 5)
    with pytest.raises(ValueError):
        calculate_compound_interest(100.0, 5.0, -5)
    with pytest.raises(ValueError):
        calculate_compound_interest(100.0, 5.0, 5, compounds_per_year=0)


def test_loan_monthly_payment_standard() -> None:
    """Test standard mortgage calculation ($300,000 at 6.0% for 30 years)."""
    payment = calculate_monthly_loan_payment(300000.0, 6.0, 30)
    assert payment == 1798.65


def test_loan_monthly_payment_zero_interest() -> None:
    """Test loan payment when interest rate is 0%."""
    payment = calculate_monthly_loan_payment(12000.0, 0.0, 1)
    assert payment == 1000.00


def test_loan_payment_invalid_inputs_raise_error() -> None:
    """Test invalid loan amounts and terms raise ValueError."""
    with pytest.raises(ValueError):
        calculate_monthly_loan_payment(0.0, 5.0, 10)
    with pytest.raises(ValueError):
        calculate_monthly_loan_payment(10000.0, 5.0, 0)
    with pytest.raises(ValueError):
        calculate_monthly_loan_payment(10000.0, -2.0, 5)


def test_amortization_schedule_completes_to_zero() -> None:
    """Test that a 2-year loan amortization schedule correctly zeroes out the remaining balance."""
    principal = 10000.0
    rate = 7.5
    years = 2
    schedule = generate_amortization_schedule(principal, rate, years)

    # 2 years = 24 monthly payments
    assert len(schedule) == 24
    # First month check
    assert schedule[0]["month"] == 1.0
    assert schedule[0]["principal"] > 0
    assert schedule[0]["interest"] > 0
    # Final month check
    assert schedule[-1]["remaining"] == 0.0


def test_amortization_schedule_total_principal_paid() -> None:
    """Test sum of principal payments equals original loan principal."""
    principal = 5000.0
    schedule = generate_amortization_schedule(principal, 5.0, 1)
    total_principal_paid = sum(row["principal"] for row in schedule)
    assert round(total_principal_paid, 2) == principal


def test_amortization_schedule_monotonically_decreasing_balance() -> None:
    """Test loan remaining balance strictly decreases each month until zero."""
    schedule = generate_amortization_schedule(15000.0, 6.5, 3)
    balances = [row["remaining"] for row in schedule]
    for i in range(len(balances) - 1):
        assert balances[i] > balances[i + 1]


def test_compound_interest_daily_compounding() -> None:
    """Test daily compounding (365 times per year) calculation."""
    balance, interest = calculate_compound_interest(1000.0, 10.0, 1, compounds_per_year=365)
    assert balance > 1100.0
    assert interest == round(balance - 1000.0, 2)


def test_loan_monthly_payment_single_year() -> None:
    """Test calculation for a 1-year auto loan at 12%."""
    payment = calculate_monthly_loan_payment(1200.0, 12.0, 1)
    # Monthly rate = 1%, (1200 * 0.01 * 1.01^12) / (1.01^12 - 1) ~= 106.62
    assert payment == 106.62
