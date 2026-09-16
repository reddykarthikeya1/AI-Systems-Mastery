#!/usr/bin/env python3
"""Module 04: Dunder (Magic) Methods Demonstration.

This script demonstrates the special abilities protocol:
__repr__, __str__, __eq__, __hash__, __add__, __len__, and __getitem__.
"""

from __future__ import annotations


class Currency:
    """Represents a monetary amount with currency code and arithmetic operator support."""

    def __init__(self, amount: float, code: str = "USD") -> None:
        self.amount = round(float(amount), 2)
        self.code = code.upper()

    def __repr__(self) -> str:
        """Unambiguous developer representation."""
        return f"Currency({self.amount}, '{self.code}')"

    def __str__(self) -> str:
        """Friendly user display string."""
        symbols = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}
        symbol = symbols.get(self.code, self.code + " ")
        return f"{symbol}{self.amount:,.2f}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Currency):
            return self.amount == other.amount and self.code == other.code
        return False

    def __hash__(self) -> int:
        return hash((self.amount, self.code))

    def __add__(self, other: Currency) -> Currency:
        if not isinstance(other, Currency) or self.code != other.code:
            raise TypeError(f"Cannot add different currencies: {self.code} and {getattr(other, 'code', type(other))}")
        return Currency(self.amount + other.amount, self.code)

    def __sub__(self, other: Currency) -> Currency:
        if not isinstance(other, Currency) or self.code != other.code:
            raise TypeError(f"Cannot subtract different currencies: {self.code} and {getattr(other, 'code', type(other))}")
        return Currency(self.amount - other.amount, self.code)

    def __mul__(self, scalar: float) -> Currency:
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Multiplier must be a number, received {type(scalar).__name__}")
        return Currency(self.amount * scalar, self.code)


class TransactionLedger:
    """Custom container demonstrating __len__, __getitem__, and __contains__."""

    def __init__(self) -> None:
        self._entries: list[Currency] = []

    def add(self, item: Currency) -> None:
        self._entries.append(item)

    def __len__(self) -> int:
        return len(self._entries)

    def __getitem__(self, index: int) -> Currency:
        return self._entries[index]

    def __contains__(self, item: Currency) -> bool:
        return item in self._entries


def main() -> None:
    print("=" * 60)
    print("  1. Custom Currency Arithmetic (__add__, __sub__, __mul__)")
    print("=" * 60)

    c1 = Currency(100.50, "USD")
    c2 = Currency(49.50, "USD")

    print(f"c1 (str)  : {c1}")
    print(f"c1 (repr) : {c1!r}")
    print(f"c1 + c2   : {c1 + c2}")
    print(f"c1 - c2   : {c1 - c2}")
    print(f"c1 * 3    : {c1 * 3}")

    print("\n" + "=" * 60)
    print("  2. Container Protocol (__len__, __getitem__, __contains__)")
    print("=" * 60)

    ledger = TransactionLedger()
    ledger.add(c1)
    ledger.add(c2)

    print(f"Total transactions in ledger (len): {len(ledger)}")
    print(f"First transaction (ledger[0])     : {ledger[0]}")
    print(f"Is c1 in ledger?                  : {c1 in ledger}")


if __name__ == "__main__":
    main()
