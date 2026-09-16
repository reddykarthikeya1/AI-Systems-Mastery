"""Beginner playground for Module 05 - SOLID Principles and Clean Architecture.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations


# ----------------------------- 1. Single responsibility: one reason to change
class OrderManagerDoingEverything:
    def process(self, order):
        total = sum(item["price"] for item in order["items"])          # pricing
        record = f"INSERT INTO orders VALUES ({order['id']}, {total})"  # persistence
        message = f"Dear {order['customer']}, your total is {total}"    # messaging
        return total, record, message


reasons_to_change = ["pricing rules", "database schema", "email wording"]
print("reasons this one class changes:", len(reasons_to_change))
assert len(reasons_to_change) == 3, "three teams, one file, three ways to collide"


# ------------------------- 2. Split it, and each piece becomes testable alone
class Pricing:
    def total(self, order):
        return sum(item["price"] for item in order["items"])


class OrderRepository:
    def __init__(self):
        self.saved = []

    def save(self, order_id, total):
        self.saved.append((order_id, total))


class Notifier:
    def __init__(self):
        self.sent = []

    def send(self, customer, total):
        self.sent.append(f"Dear {customer}, your total is {total}")


order = {"id": 1, "customer": "ana", "items": [{"price": 30}, {"price": 12}]}
pricing, repository, notifier = Pricing(), OrderRepository(), Notifier()
amount = pricing.total(order)
repository.save(order["id"], amount)
notifier.send(order["customer"], amount)

print("total:", amount)
print("saved:", repository.saved)
print("sent: ", notifier.sent)
assert amount == 42
assert pricing.total(order) == 42, "testable with no database and no mail server"


# ----------------------------------- 3. Dependency inversion: plug and socket
class InMemoryRepository:
    def __init__(self):
        self.saved = []

    def save(self, order_id, total):
        self.saved.append((order_id, total))


class PostgresRepository:
    def __init__(self):
        self.statements = []

    def save(self, order_id, total):
        self.statements.append(f"INSERT INTO orders VALUES ({order_id}, {total})")


class CheckoutService:
    # Knows only that `repository` has .save(). Nothing else.
    def __init__(self, repository):
        self.repository = repository

    def checkout(self, order):
        total = Pricing().total(order)
        self.repository.save(order["id"], total)
        return total


fake = InMemoryRepository()
real = PostgresRepository()
assert CheckoutService(fake).checkout(order) == CheckoutService(real).checkout(order)
print("with the fake:", fake.saved)
print("with postgres:", real.statements)
print("The service source code is byte-for-byte identical in both runs.")


# --------------------------- 4. Liskov: a subclass must not break the promise
class ReadOnlyRepository(InMemoryRepository):
    def save(self, order_id, total):
        raise RuntimeError("this repository does not accept writes")


def run_checkout(repository):
    return CheckoutService(repository).checkout(order)


print("with a normal repository:", run_checkout(InMemoryRepository()))
try:
    run_checkout(ReadOnlyRepository())
    raise AssertionError("expected the substitution to fail")
except RuntimeError as exc:
    print("with the 'compatible' subclass:", exc)

print("Nothing in CheckoutService is wrong. It was handed a broken promise.")


print()
print("All checks passed.")
