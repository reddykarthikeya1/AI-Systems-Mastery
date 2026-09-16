#!/usr/bin/env python3
"""Enterprise Financial Ledger Engine.

Module 08 Turnkey Project Implementation.
Target codebase for automated testing with Pytest, Mocking, and Hypothesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol


class CurrencyConverterGateway(Protocol):
    """Interface for external currency exchange rate services."""
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        ...


@dataclass
class Entry:
    """Represents an immutable ledger transaction record."""
    entry_id: str
    entry_type: str  # "CREDIT" or "DEBIT"
    amount: float
    currency: str
    timestamp: str


class FinancialLedger:
    """Enterprise double-entry compliant ledger with strict balance invariants."""

    def __init__(self, account_id: str, base_currency: str = "USD", converter: CurrencyConverterGateway | None = None) -> None:
        self.account_id = account_id
        self.base_currency = base_currency.upper()
        self.converter = converter
        self._entries: list[Entry] = []
        self._balance: float = 0.0

    @property
    def balance(self) -> float:
        return round(self._balance, 2)

    def deposit(self, amount: float, currency: str = "USD") -> Entry:
        """Deposits funds into ledger, automatically converting currency if needed."""
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive. Received: {amount}")

        currency = currency.upper()
        converted_amount = amount

        if currency != self.base_currency:
            if not self.converter:
                raise RuntimeError("Cannot accept foreign currency deposit without an active CurrencyConverterGateway.")
            rate = self.converter.get_exchange_rate(currency, self.base_currency)
            converted_amount = amount * rate

        self._balance += converted_amount
        entry = Entry(
            entry_id=f"TX-{len(self._entries) + 1:04d}",
            entry_type="CREDIT",
            amount=round(converted_amount, 2),
            currency=self.base_currency,
            timestamp=datetime.now(UTC).isoformat(),
        )
        self._entries.append(entry)
        return entry

    def withdraw(self, amount: float) -> Entry:
        """Withdraws funds from ledger, enforcing non-negative balance."""
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be positive. Received: {amount}")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds! Current balance: ${self.balance:.2f}, Requested: ${amount:.2f}")

        self._balance -= amount
        entry = Entry(
            entry_id=f"TX-{len(self._entries) + 1:04d}",
            entry_type="DEBIT",
            amount=round(amount, 2),
            currency=self.base_currency,
            timestamp=datetime.now(UTC).isoformat(),
        )
        self._entries.append(entry)
        return entry

    def get_statement(self) -> list[Entry]:
        return list(self._entries)


def main() -> None:
    print("=" * 65)
    print("      ENTERPRISE FINANCIAL LEDGER DEMO")
    print("=" * 65)

    ledger = FinancialLedger(account_id="ACC-CORP-01", base_currency="USD")
    ledger.deposit(1000.0)
    ledger.withdraw(250.0)
    ledger.deposit(500.0)

    print(f"Account: {ledger.account_id}")
    print(f"Final Balance: ${ledger.balance:,.2f}")
    print(f"Total Transactions: {len(ledger.get_statement())}")


if __name__ == "__main__":
    main()
