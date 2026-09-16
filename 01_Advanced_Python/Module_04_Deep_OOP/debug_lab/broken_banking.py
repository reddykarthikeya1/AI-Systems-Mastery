#!/usr/bin/env python3
"""Broken Banking System demonstrating OOP class attribute, hashing, and MRO traps."""

class BankAccount:
    transaction_log: list[str] = []

    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float):
        self.balance += amount
        self.transaction_log.append(f"{self.owner} deposited {amount}")

class AccountIdentifier:
    def __init__(self, account_num: str):
        self.account_num = account_num

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AccountIdentifier):
            return False
        return self.account_num == other.account_num

class BaseService:
    def log(self, msg: str):
        print(f"[Base] {msg}")

class AuditMixin(BaseService):
    def log(self, msg: str):
        BaseService.log(self, f"[Audit] {msg}")

class SecurityMixin(BaseService):
    def log(self, msg: str):
        super().log(f"[Security] {msg}")

class SecureAuditService(AuditMixin, SecurityMixin):
    pass

if __name__ == "__main__":
    acc1 = BankAccount("Alice", 100.0)
    acc2 = BankAccount("Bob", 50.0)
    acc1.deposit(25.0)
    print(f"Bob's transaction log: {acc2.transaction_log} (Expected empty, got Alice's log!)")

    id1 = AccountIdentifier("ACC-001")
    account_lookup = {}
    try:
        account_lookup[id1] = "Active"
    except TypeError as err:
        print(f"Account hash crashed: {err}")

    svc = SecureAuditService()
    svc.log("Transaction initiated")
