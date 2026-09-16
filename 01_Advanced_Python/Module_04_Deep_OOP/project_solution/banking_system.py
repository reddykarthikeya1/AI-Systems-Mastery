#!/usr/bin/env python3
"""Multi-Tier Banking & Investment System.

Module 04 Turnkey Project Implementation.
Demonstrates Deep OOP, ABCs, Dunder Arithmetic Protocols, and Properties.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Currency:
    """Represents a monetary amount with currency enforcement and operator overloading."""

    def __init__(self, amount: float | int, code: str = "USD") -> None:
        self.amount = round(float(amount), 2)
        self.code = code.upper()

    def __repr__(self) -> str:
        return f"Currency({self.amount}, '{self.code}')"

    def __str__(self) -> str:
        symbols = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}
        symbol = symbols.get(self.code, self.code + " ")
        return f"{symbol}{self.amount:,.2f}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Currency):
            return self.amount == other.amount and self.code == other.code
        return False

    def __lt__(self, other: Currency) -> bool:
        if not isinstance(other, Currency) or self.code != other.code:
            raise TypeError(f"Cannot compare different currencies: {self.code} and {getattr(other, 'code', type(other))}")
        return self.amount < other.amount

    def __le__(self, other: Currency) -> bool:
        return self < other or self == other

    def __add__(self, other: Currency) -> Currency:
        if not isinstance(other, Currency) or self.code != other.code:
            raise TypeError(f"Cannot add different currencies: {self.code} and {getattr(other, 'code', type(other))}")
        return Currency(self.amount + other.amount, self.code)

    def __sub__(self, other: Currency) -> Currency:
        if not isinstance(other, Currency) or self.code != other.code:
            raise TypeError(f"Cannot subtract different currencies: {self.code} and {getattr(other, 'code', type(other))}")
        return Currency(self.amount - other.amount, self.code)

    def __mul__(self, multiplier: float) -> Currency:
        if not isinstance(multiplier, (int, float)):
            raise TypeError(f"Multiplier must be numeric, received {type(multiplier).__name__}")
        return Currency(self.amount * multiplier, self.code)


class Account(ABC):
    """Abstract Base Class defining the contract for all bank accounts."""

    def __init__(self, account_number: str, owner_name: str, initial_balance: Currency) -> None:
        self.account_number = account_number
        self.owner_name = owner_name
        self._balance = initial_balance
        self._transactions: list[str] = [f"Account opened with initial balance: {initial_balance}"]

    @property
    def balance(self) -> Currency:
        """Read-only property for account balance."""
        return self._balance

    def deposit(self, amount: Currency) -> None:
        """Deposit funds into account."""
        if amount.amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance = self._balance + amount
        self._transactions.append(f"Deposit: +{amount} (New Balance: {self._balance})")

    @abstractmethod
    def withdraw(self, amount: Currency) -> None:
        """Abstract withdrawal method enforcing account-specific overdraft/rules."""
        pass

    @abstractmethod
    def apply_monthly_process(self) -> None:
        """Abstract monthly calculation (e.g. interest compounding or fees)."""
        pass

    def get_transaction_history(self) -> list[str]:
        return list(self._transactions)


class SavingsAccount(Account):
    """Savings account featuring annual compound yield and withdrawal limits."""

    def __init__(
        self,
        account_number: str,
        owner_name: str,
        initial_balance: Currency,
        annual_rate_percent: float = 4.5,
    ) -> None:
        super().__init__(account_number, owner_name, initial_balance)
        self.annual_rate_percent = annual_rate_percent

    def withdraw(self, amount: Currency) -> None:
        if amount.amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds: Balance is {self._balance}, attempted withdrawal {amount}")
        self._balance = self._balance - amount
        self._transactions.append(f"Withdrawal: -{amount} (New Balance: {self._balance})")

    def apply_monthly_process(self) -> None:
        monthly_rate = (self.annual_rate_percent / 100.0) / 12.0
        interest_gain = self._balance * monthly_rate
        self._balance = self._balance + interest_gain
        self._transactions.append(f"Interest Yield Applied: +{interest_gain} (New Balance: {self._balance})")


class CheckingAccount(Account):
    """Checking account supporting overdraft protection and transaction fees."""

    def __init__(
        self,
        account_number: str,
        owner_name: str,
        initial_balance: Currency,
        overdraft_limit: Currency = Currency(500.0, "USD"),
        transaction_fee: Currency = Currency(1.50, "USD"),
    ) -> None:
        super().__init__(account_number, owner_name, initial_balance)
        self.overdraft_limit = overdraft_limit
        self.transaction_fee = transaction_fee

    def withdraw(self, amount: Currency) -> None:
        if amount.amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        total_deduction = amount + self.transaction_fee
        max_allowable = self._balance + self.overdraft_limit

        if total_deduction > max_allowable:
            raise ValueError(f"Transaction exceeds overdraft limit! Available buffer: {max_allowable}")

        self._balance = self._balance - total_deduction
        self._transactions.append(f"Withdrawal: -{amount} [Fee: {self.transaction_fee}] (New Balance: {self._balance})")

    def apply_monthly_process(self) -> None:
        # Maintenance logic (if any)
        pass


class Bank:
    """Manages bank accounts and executes multi-account transactions."""

    def __init__(self, bank_name: str = "Apex National Bank") -> None:
        self.bank_name = bank_name
        self._accounts: dict[str, Account] = {}

    def add_account(self, account: Account) -> None:
        self._accounts[account.account_number] = account

    def get_account(self, account_number: str) -> Account | None:
        return self._accounts.get(account_number)

    def transfer(self, from_acc_num: str, to_acc_num: str, amount: Currency) -> bool:
        from_acc = self._accounts.get(from_acc_num)
        to_acc = self._accounts.get(to_acc_num)
        if not from_acc or not to_acc:
            raise ValueError("Invalid account number in transfer request.")

        # Atomic transfer
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        return True

    def calculate_total_deposits(self, currency_code: str = "USD") -> Currency:
        total = Currency(0.0, currency_code)
        for acc in self._accounts.values():
            if acc.balance.code == currency_code and acc.balance.amount > 0:
                total = total + acc.balance
        return total


def main() -> None:
    print("=" * 65)
    print("        APEX BANKING & INVESTMENT MANAGEMENT SYSTEM")
    print("=" * 65)

    bank = Bank()

    # Create Accounts
    alice_savings = SavingsAccount("SAV-101", "Alice Vance", Currency(5000.0, "USD"), annual_rate_percent=6.0)
    bob_checking = CheckingAccount("CHK-202", "Bob Smith", Currency(1000.0, "USD"))

    bank.add_account(alice_savings)
    bank.add_account(bob_checking)

    print("\n1. Applying Monthly Interest to Savings Account:")
    print(f"Alice's Balance Before: {alice_savings.balance}")
    alice_savings.apply_monthly_process()
    print(f"Alice's Balance After : {alice_savings.balance}")

    print("\n2. Executing Funds Transfer from Alice to Bob ($1,500.00):")
    bank.transfer("SAV-101", "CHK-202", Currency(1500.0, "USD"))
    print(f"Alice Savings Balance: {alice_savings.balance}")
    print(f"Bob Checking Balance : {bob_checking.balance}")

    print("\n3. Bank-Wide Total Deposits:")
    print(f"Total Bank Reserves: {bank.calculate_total_deposits('USD')}")


if __name__ == "__main__":
    main()
