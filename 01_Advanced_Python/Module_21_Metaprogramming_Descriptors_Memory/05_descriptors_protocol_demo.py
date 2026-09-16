#!/usr/bin/env python3
"""Module 19: Python Descriptor Protocol Demonstration.

This script demonstrates data descriptors vs non-data descriptors and how
attribute lookup precedence operates.
"""

from __future__ import annotations


class IntegerField:
    """Data Descriptor enforcing integer values."""

    def __set_name__(self, owner: type, name: str) -> None:
        self.storage_name = f"_{name}"
        self.field_name = name

    def __get__(self, instance: object, owner: type) -> object:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, 0)

    def __set__(self, instance: object, value: object) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Field '{self.field_name}' must be an integer (Got {type(value).__name__})")
        setattr(instance, self.storage_name, value)


class BankAccount:
    balance = IntegerField()

    def __init__(self, initial_balance: int) -> None:
        self.balance = initial_balance


def main() -> None:
    print("=" * 60)
    print("  Python Descriptor Protocol Demonstration")
    print("=" * 60)

    acc = BankAccount(500)
    print(f"Initial Account Balance: ${acc.balance}")

    acc.balance = 750
    print(f"Updated Balance: ${acc.balance}")

    try:
        acc.balance = "one million"
    except TypeError as err:
        print(f"Caught expected validation error: {err}")


if __name__ == "__main__":
    main()
