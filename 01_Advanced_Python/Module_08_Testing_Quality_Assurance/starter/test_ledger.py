"""Production-Grade Automated Test Suite for FinancialLedger.

Module 08 Turnkey Project Test Suite.
Demonstrates Pytest Fixtures, Parametrization, Mocking, and Hypothesis Property Testing.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from hypothesis import given
from hypothesis import strategies as st
from ledger import CurrencyConverterGateway, FinancialLedger


# 1. Pytest Fixtures
@pytest.fixture
def empty_ledger() -> FinancialLedger:
    """Fixture providing a clean zero-balance ledger."""
    return FinancialLedger(account_id="TEST-001", base_currency="USD")


@pytest.fixture
def funded_ledger(empty_ledger: FinancialLedger) -> FinancialLedger:
    """Fixture providing a pre-funded ledger with $1,000.00 balance."""
    empty_ledger.deposit(1000.0)
    return empty_ledger


# 2. Parametrized Table-Driven Tests
@pytest.mark.parametrize("deposit_amount, withdraw_amount, expected_balance", [
    (500.0, 200.0, 300.0),
    (100.0, 100.0, 0.0),
    (1250.75, 250.50, 1000.25),
    (0.01, 0.01, 0.0),
])
def test_deposit_and_withdraw_math(
    empty_ledger: FinancialLedger,
    deposit_amount: float,
    withdraw_amount: float,
    expected_balance: float,
) -> None:
    empty_ledger.deposit(deposit_amount)
    empty_ledger.withdraw(withdraw_amount)
    assert empty_ledger.balance == expected_balance


# 3. Error Validation Tests
def test_negative_deposit_raises_error(empty_ledger: FinancialLedger) -> None:
    with pytest.raises(ValueError) as exc_info:
        empty_ledger.deposit(-50.0)
    assert "Deposit amount must be positive" in str(exc_info.value)


def test_overdraw_raises_insufficient_funds(funded_ledger: FinancialLedger) -> None:
    with pytest.raises(ValueError) as exc_info:
        funded_ledger.withdraw(1500.0)
    assert "Insufficient funds" in str(exc_info.value)


# 4. Mocking External Currency Converter Gateway
def test_foreign_currency_deposit_with_mock() -> None:
    mock_gateway = MagicMock(spec=CurrencyConverterGateway)
    # EUR to USD rate: 1.10
    mock_gateway.get_exchange_rate.return_value = 1.10

    ledger = FinancialLedger(account_id="CORP-EUR", base_currency="USD", converter=mock_gateway)
    entry = ledger.deposit(100.0, currency="EUR")

    # 100 EUR * 1.10 = 110 USD
    assert ledger.balance == 110.0
    assert entry.amount == 110.0
    mock_gateway.get_exchange_rate.assert_called_once_with("EUR", "USD")


def test_foreign_currency_missing_converter_raises_runtime_error() -> None:
    ledger = FinancialLedger(account_id="CORP-NO-CONV", base_currency="USD", converter=None)
    with pytest.raises(RuntimeError):
        ledger.deposit(100.0, currency="EUR")


# 5. Property-Based Testing with Hypothesis
@given(st.lists(st.floats(min_value=0.01, max_value=1000.0, allow_nan=False, allow_infinity=False), min_size=1, max_size=50))
def test_balance_invariant_matches_sum_of_deposits(deposit_amounts: list[float]) -> None:
    """Property: The final balance must always equal the exact rounded sum of all deposits."""
    ledger = FinancialLedger(account_id="PROP-TEST", base_currency="USD")
    for amount in deposit_amounts:
        ledger.deposit(amount)

    expected_total = round(sum(deposit_amounts), 2)
    assert ledger.balance == expected_total
