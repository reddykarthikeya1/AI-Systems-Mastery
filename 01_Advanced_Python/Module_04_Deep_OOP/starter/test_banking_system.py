"""Unit tests for the Multi-Tier Banking & Investment System."""

from __future__ import annotations

import pytest
from banking_system import Bank, CheckingAccount, Currency, SavingsAccount


def test_currency_arithmetic_and_comparison() -> None:
    """Test Currency dunder operations."""
    c1 = Currency(100.0, "USD")
    c2 = Currency(50.0, "USD")

    assert (c1 + c2) == Currency(150.0, "USD")
    assert (c1 - c2) == Currency(50.0, "USD")
    assert (c1 * 2) == Currency(200.0, "USD")
    assert c2 < c1
    assert str(c1) == "$100.00"

    # Currency mismatch error
    with pytest.raises(TypeError):
        _ = c1 + Currency(50.0, "EUR")


def test_savings_account_deposit_and_interest() -> None:
    """Test savings account interest yield and withdrawal restrictions."""
    acc = SavingsAccount("SAV-1", "Test User", Currency(1200.0, "USD"), annual_rate_percent=12.0)

    # 12% annual = 1% monthly -> 1% of 1200 is 12.00
    acc.apply_monthly_process()
    assert acc.balance == Currency(1212.0, "USD")

    acc.withdraw(Currency(212.0, "USD"))
    assert acc.balance == Currency(1000.0, "USD")

    # Insufficient funds error
    with pytest.raises(ValueError):
        acc.withdraw(Currency(2000.0, "USD"))


def test_checking_account_overdraft_and_fees() -> None:
    """Test checking account overdraft limits and fees."""
    # Balance 100, Overdraft limit 50, fee 2.00 -> total allowable deduction 150
    chk = CheckingAccount(
        "CHK-1",
        "Test User",
        Currency(100.0, "USD"),
        overdraft_limit=Currency(50.0, "USD"),
        transaction_fee=Currency(2.00, "USD"),
    )

    # Withdraw 120 + 2 fee = 122 deduction -> balance becomes -22.00
    chk.withdraw(Currency(120.0, "USD"))
    assert chk.balance == Currency(-22.0, "USD")

    # Attempting to exceed overdraft limit raises ValueError
    with pytest.raises(ValueError):
        chk.withdraw(Currency(50.0, "USD"))


def test_bank_transfers_and_aggregations() -> None:
    """Test Bank container transfers and aggregate calculations."""
    bank = Bank()
    acc_a = SavingsAccount("ACC-A", "Alice", Currency(1000.0, "USD"))
    acc_b = CheckingAccount("ACC-B", "Bob", Currency(200.0, "USD"), transaction_fee=Currency(0.0, "USD"))

    bank.add_account(acc_a)
    bank.add_account(acc_b)

    # Transfer $300 from Alice to Bob
    success = bank.transfer("ACC-A", "ACC-B", Currency(300.0, "USD"))
    assert success is True
    assert acc_a.balance == Currency(700.0, "USD")
    assert acc_b.balance == Currency(500.0, "USD")

    # Total deposits across bank
    total_usd = bank.calculate_total_deposits("USD")
    assert total_usd == Currency(1200.0, "USD")


def test_currency_invalid_multiplier_type() -> None:
    """Test multiplying Currency by non-numeric raises TypeError."""
    c = Currency(50.0, "USD")
    with pytest.raises(TypeError, match="Multiplier must be numeric"):
        _ = c * "two"  # type: ignore


def test_currency_comparison_different_codes_raises_type_error() -> None:
    """Test comparing different currency codes raises TypeError."""
    c_usd = Currency(100.0, "USD")
    c_eur = Currency(100.0, "EUR")
    with pytest.raises(TypeError, match="Cannot compare different currencies"):
        _ = c_usd < c_eur


def test_account_negative_deposit_raises_value_error() -> None:
    """Test depositing zero or negative amount raises ValueError."""
    acc = SavingsAccount("SAV-2", "Bob", Currency(500.0, "USD"))
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acc.deposit(Currency(-50.0, "USD"))
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acc.deposit(Currency(0.0, "USD"))


def test_account_transaction_history_tracking() -> None:
    """Test account transaction history records deposits and withdrawals."""
    acc = SavingsAccount("SAV-3", "Charlie", Currency(200.0, "USD"))
    acc.deposit(Currency(100.0, "USD"))
    history = acc.get_transaction_history()
    assert len(history) >= 2
    assert any("Deposit" in h for h in history)


def test_bank_get_account_retrieval() -> None:
    """Test Bank get_account returns matching account or None."""
    bank = Bank()
    acc = SavingsAccount("SAV-99", "Eve", Currency(400.0, "USD"))
    bank.add_account(acc)
    assert bank.get_account("SAV-99") is acc
    assert bank.get_account("NONEXISTENT") is None


def test_bank_transfer_invalid_account_raises_error() -> None:
    """Test transferring to or from invalid account number raises ValueError."""
    bank = Bank()
    acc = SavingsAccount("SAV-10", "User", Currency(100.0, "USD"))
    bank.add_account(acc)
    with pytest.raises(ValueError, match="Invalid account number"):
        bank.transfer("SAV-10", "MISSING", Currency(50.0, "USD"))
    with pytest.raises(ValueError, match="Invalid account number"):
        bank.transfer("MISSING", "SAV-10", Currency(50.0, "USD"))


def test_currency_repr_and_equality() -> None:
    """Test Currency repr string and equality semantics."""
    c1 = Currency(42.50, "USD")
    c2 = Currency(42.50, "USD")
    c3 = Currency(42.50, "EUR")
    assert repr(c1) == "Currency(42.5, 'USD')"
    assert c1 == c2
    assert c1 != c3
    assert c1 != "not-currency"
